from contextlib import contextmanager
import os

from shmir import (
    settings,
    utils
)


@contextmanager
def mfold_path(task_id):
    programm_path = os.getcwd()

    tmp_dirname = utils.get_dirname(task_id)

    os.chdir(tmp_dirname)

    yield tmp_dirname

    os.chdir(programm_path)


@contextmanager
def blast_path():
    old_path = os.getcwd()
    os.chdir(settings.BLAST_PATH)

    yield

    os.chdir(old_path)
