"""
.. module:: shmir.context_managers
    :synopsis: Module for context managers
"""
from contextlib import contextmanager
import os

from shmir import (
    settings,
    utils
)


def generic_path(path):
    """Function which changes current path to given path

    Args:
        path(str): path where interpreter should be
    """
    old_path = os.getcwd()
    os.chdir(path)

    yield path

    os.chdir(old_path)


@contextmanager
def mfold_path(task_id):
    """Context manager which changes path for mfold tasks

    Args:
        task_id: id of mfold task
    """
    for path in generic_path(utils.get_dirname(task_id)):
        yield path


@contextmanager
def blast_path():
    """
    Context manager which changes path for blast executions
    """
    for _ in generic_path(settings.BLAST_PATH):
        yield
