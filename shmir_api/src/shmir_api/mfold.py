from os import chdir, fork, waitpid, path, makedirs, execl

from os.path import dirname
from os.path import join

from datetime import datetime

from settings import MFOLD_PATH


def delegate_mfold(input):
    """
    Executes mfold in order to generate appropriate files
    """
    current_datetime = datetime.now().strftime('%H:%M:%S-%d-%m-%y')

    mfold_dirname = "mfold_files"
    tmp_dirname = join(dirname(__file__), mfold_dirname, current_datetime)

    if not path.exists(tmp_dirname):
        makedirs(tmp_dirname)
    chdir(tmp_dirname)

    with open(current_datetime, "w") as f:
        f.write(input)

    pid = fork()

    if pid == 0:
        execl(MFOLD_PATH, 'mfold', 'SEQ=%s P=1' % current_datetime)

    waitpid(pid, 0)

    return map(
        lambda path: join(tmp_dirname, path.format(current_datetime)),
        ["{}_1.pdf", "{}_1.ss"]
    )
