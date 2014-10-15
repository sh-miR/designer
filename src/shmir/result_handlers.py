"""
.. module:: shmir.result_handlers
    :synopsis: Module with handlers for zip files
"""

import os
from email import encoders
from email.mime.base import MIMEBase

from shmir import app
from shmir.utils import get_zip_path


def zip_file_mfold(path):
    """Function which creates zip_msg to send via email

    Args:
        path: path of zip file

    Returns:
        tuple of zip message
    """
    zip_msg = MIMEBase('application', 'zip')
    with open(path, 'r') as zip_file:
        zip_msg.set_payload(zip_file.read())
    encoders.encode_base64(zip_msg)
    zip_msg.add_header('Content-Disposition', 'attachment',
                       filename=os.path.basename(path))

    return zip_msg,


def zip_files_from_sirna(struct):
    """Function which generates email msg from siRNA

    Args:
        struct: sh-miR struct

    Returns:
        zip message
    """
    for element in struct:
        task_id = element[-1]
        with app.app_context():
            path = get_zip_path(task_id, task_id)

        zip_msg = MIMEBase('application', 'zip')
        with open(path) as zip_file:
            zip_msg.set_payload(zip_file.read())
        encoders.encode_base64(zip_msg)
        zip_msg.add_header('Content-Disposition', 'attachment',
                           filename=os.path.basename(path))

        yield zip_msg
