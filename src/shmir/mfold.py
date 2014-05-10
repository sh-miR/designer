from os import (
    fork,
    waitpid,
    execl,
    path
)
from datetime import datetime
from zipfile import ZipFile

from shmir.contextmanagers import mfold_path
from shmir.celery import celery
from shmir.settings import (
    MFOLD_PATH,
)


@celery.task(bind=True)
def delegate_mfold(self, input, current_datetime=None):
    """
    Executes mfold in order to generate appropriate files
    """
    #if not current_datetime:
    #    current_datetime = datetime.now().strftime('%H:%M:%S-%d-%m-%y')

    with mfold_path(self.request.id) as tmp_dirname:
        with open(self.request.id, "w") as f:
            f.write(input)

        pid = fork()

        if pid == 0:
            execl(MFOLD_PATH, 'mfold', 'SEQ={} P=1'.format(self.request.id))

        waitpid(pid, 0)

        result = map(
            lambda mfold_path: path.join(
                tmp_dirname, mfold_path.format(self.request.id)
            ),
            ["{}_1.pdf", "{}_1.ss"]
        )

    return result


'''def zipped_mfold(input):
    current_datetime = datetime.now().strftime('%H:%M:%S-%d-%m-%y')
    files = delegate_mfold(input, current_datetime)

    with mfold_path(current_datetime) as tmp_dirname:
        zipname = "{}.zip".format(current_datetime)

        with ZipFile(zipname, 'w') as mfold_zip:
            for filename in map(path.basename, files):
                mfold_zip.write(filename)

        result = path.join(tmp_dirname, zipname)

    return result'''


def zipped_mfold(current_datetime, files):
    with mfold_path(current_datetime) as tmp_dirname:
        zipname = "{}.zip".format(current_datetime)

        with ZipFile(zipname, 'w') as mfold_zip:
            for filename in map(path.basename, files):
                mfold_zip.write(filename)

        result = path.join(tmp_dirname, zipname)

    return result
