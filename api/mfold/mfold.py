from os import chdir, execlp, mkdir, fork, waitpid

from os.path import dirname
from os.path import join

from datetime import datetime

from zipfile import ZipFile


def mfold(input):
    """
    Executing mfold to create appropriate files

    """
    current_datetime = datetime.now().strftime('%H:%M:%S-%d-%m-%y')

    tmp_dirname = join(dirname(__file__), current_datetime)

    mkdir(tmp_dirname)
    chdir(tmp_dirname)

    with open(current_datetime, "w") as f:
        f.write(input)

    pid = fork()
    if pid == 0:
        execlp("mfold", "mfold", "SEQ=%s" % current_datetime)
    waitpid(pid, 0)

    zipname = "%s.zip" % current_datetime

    with ZipFile(zipname, 'w') as mfold_zip:
        mfold_zip.write("%s_1.pdf" % current_datetime)
        mfold_zip.write("%s_1.ss" % current_datetime)

    return join(tmp_dirname, zipname)
