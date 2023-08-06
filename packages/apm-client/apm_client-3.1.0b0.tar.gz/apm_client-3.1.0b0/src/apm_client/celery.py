# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import datetime as dt
import logging

from celery.signals import before_task_publish, task_failure, task_postrun, task_prerun

try:
    import django

    if django.VERSION < (3, 1):
        from django.views.debug import get_safe_settings
    else:
        from django.views.debug import SafeExceptionReporterFilter

        def get_safe_settings():
            return SafeExceptionReporterFilter().get_safe_settings()


except ImportError:
    # Django not installed
    get_safe_settings = None

import apm_client.core
from apm_client.compat import datetime_to_timestamp
from apm_client.core.config import scout_config
from apm_client.core.error import ErrorMonitor
from apm_client.core.tracked_request import TrackedRequest

logger = logging.getLogger(__name__)


def before_task_publish_callback(headers=None, properties=None, **kwargs):
    if "scout_task_start" not in headers:
        headers["scout_task_start"] = datetime_to_timestamp(dt.datetime.utcnow())


def task_prerun_callback(task=None, **kwargs):
    tracked_request = TrackedRequest.instance()
    tracked_request.is_real_request = True

    start = getattr(task.request, "scout_task_start", None)
    if start is not None:
        now = datetime_to_timestamp(dt.datetime.utcnow())
        try:
            queue_time = now - start
        except TypeError:
            pass
        else:
            tracked_request.tag("queue_time", queue_time)

    task_id = getattr(task.request, "id", None)
    if task_id:
        tracked_request.tag("task_id", task_id)
    parent_task_id = getattr(task.request, "parent_id", None)
    if parent_task_id:
        tracked_request.tag("parent_task_id", parent_task_id)

    delivery_info = task.request.delivery_info
    tracked_request.tag("is_eager", delivery_info.get("is_eager", False))
    tracked_request.tag("exchange", delivery_info.get("exchange", "unknown"))
    tracked_request.tag("priority", delivery_info.get("priority", "unknown"))
    tracked_request.tag("routing_key", delivery_info.get("routing_key", "unknown"))
    tracked_request.tag("queue", delivery_info.get("queue", "unknown"))

    tracked_request.start_span(operation=("Job/" + task.name))


def task_postrun_callback(task=None, **kwargs):
    tracked_request = TrackedRequest.instance()
    tracked_request.stop_span()


def task_failure_callback(
    sender,
    task_id=None,
    exception=None,
    args=None,
    kwargs=None,
    traceback=None,
    **remaining
):
    tracked_request = TrackedRequest.instance()
    tracked_request.tag("error", "true")

    custom_controller = sender.name
    custom_params = {
        "celery": {
            "task_id": task_id,
            "args": args,
            "kwargs": kwargs,
        }
    }

    # Look up the django settings if populated.
    environment = None
    if get_safe_settings:
        try:
            environment = get_safe_settings()
        except django.core.exceptions.ImproperlyConfigured as exc:
            # Django not setup correctly
            logger.debug(
                "Celery integration does not have django configured properly: %r", exc
            )
            pass
        except Exception as exc:
            logger.debug(
                "Celery task_failure callback exception: %r", exc, exc_info=exc
            )
            pass

    exc_info = (exception.__class__, exception, traceback)
    ErrorMonitor.send(
        exc_info,
        environment=environment,
        custom_params=custom_params,
        custom_controller=custom_controller,
    )


def install(app=None):
    if app is not None:
        copy_configuration(app)

    installed = apm_client.core.install()
    if not installed:
        return

    before_task_publish.connect(before_task_publish_callback)
    task_prerun.connect(task_prerun_callback)
    task_failure.connect(task_failure_callback)
    task_postrun.connect(task_postrun_callback)


def copy_configuration(app):
    prefix = "scout_"
    prefix_len = len(prefix)

    to_set = {}
    for key, value in app.conf.items():
        key_lower = key.lower()
        if key_lower.startswith(prefix) and len(key_lower) > prefix_len:
            scout_key = key_lower[prefix_len:]
            to_set[scout_key] = value

    scout_config.set(**to_set)


def uninstall():
    before_task_publish.disconnect(before_task_publish_callback)
    task_prerun.disconnect(task_prerun_callback)
    task_postrun.disconnect(task_postrun_callback)
    task_failure.disconnect(task_failure_callback)
