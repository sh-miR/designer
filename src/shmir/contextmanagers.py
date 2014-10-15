from contextlib import contextmanager
import os

from shmir import (
    settings,
    utils
)


def generic_path(path):
    old_path = os.getcwd()
    os.chdir(path)

    yield path

    os.chdir(old_path)


@contextmanager
def mfold_path(task_id):
    for path in generic_path(utils.get_dirname(task_id)):
        yield path


@contextmanager
def blast_path():
    for _ in generic_path(settings.BLAST_PATH):
        yield
