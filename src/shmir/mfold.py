"""
.. module:: shmir.mfold
    :synopsis: Module which handels mfold
"""
import os
from zipfile import ZipFile

from shmir.decorators import catch_errors
from shmir.designer.errors import NoResultError
from shmir.contextmanagers import mfold_path
from shmir.async import task
from shmir.decorators import send_email
from shmir.result_handlers import zip_file_mfold
from shmir.settings import MFOLD_PATH
from shmir.utils import remove_error_folding


def zip_file(task_id, files, tmp_dirname):
    """Zipping mfold files of specific task

    Args:
        task_id: Id of task generated via RESTful API
        files(iterable): files folded via mfold which will be zipped
        tmp_dirname: temporary dirname

    Returns:
        path of zipped file
    """
    zipname = "{}.zip".format(task_id)

    with ZipFile(zipname, 'w') as mfold_zip:
        for filename in files:
            mfold_zip.write(
                filename, "{}/{}".format(*filename.split('/')[-2:])
            )

    result = os.path.join(tmp_dirname, zipname)

    return result


def execute(directory, sequence, to_zip=True):
    """Function which executes mfold

    Args:
        directory: directory in which mfold is executed & output files are stored
        sequence(str): sequence to be folded via mfold
        to_zip(bool): tells if files should be zipped (default: True)

    Returns:
        Path of foleded files
    """
    with mfold_path(directory) as tmp_dirname:
        with open('sequence', "w") as f:
            f.write(sequence)

        pid = os.fork()

        if pid == 0:
            os.execl(MFOLD_PATH, 'mfold', 'SEQ=sequence')

        process_id, status = os.waitpid(pid, 0)
        # Status in 0 - 255
        status = (status & 0xff00) >> 8

        if status == 0:
            result = map(
                lambda mfold_path: os.path.join(
                    tmp_dirname, mfold_path.format('sequence')
                ),
                ["{}_1.pdf", "{}_1.ss"]
            )

            if to_zip:
                result = zip_file(directory, result, tmp_dirname)

    if status != 0:
        remove_error_folding(directory)
        raise NoResultError("No foldings for %s" % sequence)

    return result


@task(bind=True)
@catch_errors(NoResultError)
@send_email(file_handler=zip_file_mfold)
def delegate(self, sequence):
    """Executes mfold in order to generate appropriate files
    Args:
        sequence: sequence to be folded
    Returns:
        Path of folded files
    """
    return execute(self.request.id, sequence)
