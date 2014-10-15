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
    """Creates json object from given error

    Args:
        error(str): error message
    Returns:
        Json object
    """
    return jsonify(error=error)


def get_dirname(task_id):
    """Function which gets dirname of folded sequence by task id

    Args:
        task_id: Id of task generated via RESTful API

    Returns:
        directory name (str)
    """
    dirname = os.path.join(MFOLD_FILES, task_id)

    if not os.path.exists(dirname):
        os.makedirs(dirname)

    return dirname


@cache.memoize()
def get_zip_path(path, task_id):
    """Gets path of zip via mfold task id

    Args:
        path: path where zip is
        task_id: Id of task and name of zip

    Returns:
        Path where zip is
    """
    return os.path.join(get_dirname(path), '{}.zip'.format(task_id))


def remove_bad_foldings(path_id, good_ids):
    """Removes all folded structures which were not choosen

    Args:
        path_id: name of path where we should delete bad foldings
        good_ids(list): list of all ids which should be not deleted
    """
    for dirname in glob.glob(os.path.join(MFOLD_FILES, path_id)):
        if not os.path.basename(dirname) in good_ids:
            shutil.rmtree(dirname)


def remove_error_folding(path_id):
    """Removes one specific folding from given path_id

    Args:
        path_id: name of path where mfold file is
    """
    shutil.rmtree(os.path.join(MFOLD_FILES, path_id))
