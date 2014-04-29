from contextlib import contextmanager
from os import (
    chdir,
    getcwd,
    makedirs,
    path
)

from settings import MFOLD_FILES


@contextmanager
def mfold_path(current_datetime):
    programm_path = getcwd()

    tmp_dirname = path.join(MFOLD_FILES, current_datetime)

    if not path.exists(tmp_dirname):
        makedirs(tmp_dirname)
    chdir(tmp_dirname)

    yield tmp_dirname

    chdir(programm_path)
