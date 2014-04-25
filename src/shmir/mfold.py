from os import (
    chdir,
    fork,
    waitpid,
    path,
    makedirs,
    execl,
    getcwd,
)
from os.path import (
    dirname,
    join,
    basename,
)
from datetime import datetime

from zipfile import ZipFile
from settings import (
    MFOLD_PATH,
    MFOLD_FILES,
)


def delegate_mfold(input, current_datetime=None):
    """
    Executes mfold in order to generate appropriate files
    """
    programm_path = getcwd()
    if not current_datetime:
        current_datetime = datetime.now().strftime('%H:%M:%S-%d-%m-%y')

    tmp_dirname = join(MFOLD_FILES, current_datetime)

    if not path.exists(tmp_dirname):
        makedirs(tmp_dirname)
    chdir(tmp_dirname)

    with open(current_datetime, "w") as f:
        f.write(input)

    pid = fork()

    if pid == 0:
        execl(MFOLD_PATH, 'mfold', 'SEQ={} P=1'.format(current_datetime))

    waitpid(pid, 0)

    chdir(programm_path)

    return map(
        lambda path: join(tmp_dirname, path.format(current_datetime)),
        ["{}_1.pdf", "{}_1.ss"]
    )


def zipped_mfold(input):
    current_datetime = datetime.now().strftime('%H:%M:%S-%d-%m-%y')
    files = delegate_mfold(input, current_datetime)
    tmp_dirname = dirname(files[0])

    zipname = "{}.zip".format(current_datetime)

    with ZipFile(zipname, 'w') as mfold_zip:
        for filename in map(basename, files):
            mfold_zip.write(filename)

    return join(tmp_dirname, zipname)
