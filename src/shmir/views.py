"""
Handlers

"""

from flask import send_file

from shmir import app
from shmir.celery import get_async_result
from shmir.decorators import require_json
from shmir.mfold import (
    delegate_mfold,
    zipped_mfold
)


@app.route('/mfold', methods=['POST'])
@require_json()
def mfold_d(data=None, **kwargs):
    resource = delegate_mfold.delay(data)
    return {'task_id': resource.task_id}


@app.route("/mfold/result/<task_id>")
def mfold_result(task_id):
    retval = get_async_result(delegate_mfold, task_id)
    return repr(retval)

'''@app.route('/mfold', methods=['POST'])
@require_json(jsonify=False)
def get_mfold(data=None, **kwargs):
    filename = zipped_mfold(data)

    return send_file(filename)'''
