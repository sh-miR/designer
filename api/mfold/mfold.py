from os import chdir
from os import execlp
from os import mkdir

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

    execlp("mfold", "seq='mfold_input'")

    with ZipFile("%s.zip" % current_datetime) as mfold_zip:
        mfold_zip.write("mfold.pdf")
        mfold_zip.write("mfold.ss")

    with open("%s.zip" % current_datetime, "rb") as f:
        result = f.read()

    return result
