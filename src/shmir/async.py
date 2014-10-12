from __future__ import absolute_import

from celery import Celery
from celery.exceptions import TimeoutError
from kombu import Exchange, Queue

from shmir import app
from shmir.settings import (
    CELERY_BROKER,
    CELERY_RESULT_BACKEND
)

__all__ = ['celery', 'get_async_result', 'task']


def make_celery(app_obj):
    """
    Wraps Celery with app context and settings
    """
    celery = Celery(
        app_obj.import_name,
        broker=CELERY_BROKER,
        backend=CELERY_RESULT_BACKEND
    )
    celery.conf.update(app_obj.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app_obj.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    celery.conf.update(
        CELERY_TASK_SERIALIZER='pickle',
        CELERY_TIMEZONE="Europe/Warsaw",
        CELERY_QUEUES=(
            Queue('design', Exchange('design')),
            Queue('score', Exchange('score')),
            Queue('subtasks', Exchange('subtasks')),
        )
    )

    return celery


celery = make_celery(app)
task = celery.task


def _get_async_result(result, timeout=1.0, only_status=False):
    """
    Excepting TimeoutError and handling failures of every result
    """
    if result.failed():
        return {'status': 'fail'}

    try:
        data = result.get(timeout=timeout)
    except TimeoutError:
        return {'status': 'in progress'}

    if isinstance(data, dict) and data.get('status') == 'error':
        response = data
    else:
        response = {'status': 'ok'}

        if not only_status:
            response['data'] = {'result': data}

    return response


def get_async_result(task, task_id, timeout=1.0, only_status=False):
    """
    Gets AsyncResult of task, excepting TimeoutError and handling failures
    """
    result = task.AsyncResult(task_id)
    return _get_async_result(result, timeout=timeout, only_status=only_status)
