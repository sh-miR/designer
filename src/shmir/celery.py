from __future__ import absolute_import

from celery import Celery
from celery.exceptions import TimeoutError

from shmir import app
from shmir.settings import (
    CELERY_BROKER,
    CELERY_RESULT_BACKEND
)

__all__ = ['celery', 'get_async_result']


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

    return celery


celery = make_celery(app)


def get_async_result(task, task_id, timeout=1.0):
    """
    Gets AsyncResult of task, excepting TimeoutError and handling failures
    """
    if task.AsyncResult(task_id).failed():
        return {'status': 'fail'}

    try:
        return {
            'status': 'ok',
            'data': task.AsyncResult(task_id).get(timeout=timeout)
        }
    except TimeoutError:
        return {'status': 'in progress'}
