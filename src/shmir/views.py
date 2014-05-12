"""
Handlers

"""

from flask import (
    jsonify,
    send_file
)

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


@app.route('/mfold/result/<task_id>')
def mfold_result(task_id):
    return jsonify(get_async_result(delegate_mfold, task_id))


@app.route('/mfold/file/<task_id>')
def mfold_files(task_id):
    try:
        files = get_async_result(delegate_mfold, task_id)['data']
    except KeyError:
        return jsonify({
            'status': 'error', 'error': 'Task is not ready or has failed'
        })
    zip_file = zipped_mfold(task_id, files)

    return send_file(zip_file)
