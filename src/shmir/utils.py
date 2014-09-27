"""
Utilies for handling json
"""

import os

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
def get_zip_path(task_id):
    return os.path.join(get_dirname(task_id), '{}.zip'.format(task_id))
