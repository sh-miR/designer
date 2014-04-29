from os import (
    fork,
    waitpid,
    execl,
    path
)
from datetime import datetime

from contextmanagers import mfold_path
from zipfile import ZipFile
from settings import (
    MFOLD_PATH,
)


def delegate_mfold(input, current_datetime=None):
    """
    Executes mfold in order to generate appropriate files
    """
    if not current_datetime:
        current_datetime = datetime.now().strftime('%H:%M:%S-%d-%m-%y')

    with mfold_path(current_datetime) as tmp_dirname:
        with open(current_datetime, "w") as f:
            f.write(input)

        pid = fork()

        if pid == 0:
            execl(MFOLD_PATH, 'mfold', 'SEQ={} P=1'.format(current_datetime))

        waitpid(pid, 0)

        result = map(
            lambda mfold_path: path.join(
                tmp_dirname, mfold_path.format(current_datetime)
            ),
            ["{}_1.pdf", "{}_1.ss"]
        )

    return result


def zipped_mfold(input):
    current_datetime = datetime.now().strftime('%H:%M:%S-%d-%m-%y')
    files = delegate_mfold(input, current_datetime)

    with mfold_path(current_datetime) as tmp_dirname:
        zipname = "{}.zip".format(current_datetime)

        with ZipFile(zipname, 'w') as mfold_zip:
            for filename in map(path.basename, files):
                mfold_zip.write(filename)

        result = path.join(tmp_dirname, zipname)

    return result
