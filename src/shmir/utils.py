"""
Utilies for handling json
"""

import os
import shutil
import glob

from flask import jsonify

from shmir import cache
from shmir.settings import MFOLD_FILES


def json_error(error):
    """Input: string
    Output: dictionary"""
    return jsonify(error=error)


def get_dirname(task_id):
    dirname = os.path.join(MFOLD_FILES, task_id)

    if not os.path.exists(dirname):
        os.makedirs(dirname)

    return dirname


@cache.cached()
def get_zip_path(path, task_id):
    return os.path.join(get_dirname(path), '{}.zip'.format(task_id))


def remove_bad_foldings(path_id, good_ids):
    for dirname in glob.glob(os.path.join(MFOLD_FILES, path_id)):
        if not os.path.basename(dirname) in good_ids:
            shutil.rmtree(dirname)
