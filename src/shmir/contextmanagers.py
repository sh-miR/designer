from contextlib import contextmanager
import os

from shmir import utils


@contextmanager
def mfold_path(task_id):
    programm_path = os.getcwd()

    tmp_dirname = utils.get_dirname(task_id)

    os.chdir(tmp_dirname)

    yield tmp_dirname

    os.chdir(programm_path)
