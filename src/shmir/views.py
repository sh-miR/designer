"""
Handlers

"""

from flask import (
    jsonify,
    send_file
)

from shmir import app
from shmir.celery import get_async_result
from shmir.designer.design import design_and_score
from shmir.mfold import (
    delegate_mfold,
    zipped_mfold
)


@app.route('/mfold/status/<task_id>')
def mfold_task_status(task_id):
    return jsonify(get_async_result(delegate_mfold, task_id, only_status=True))


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


@app.route('/mfold/<data>')
def mfold_data_handler(data):
    resource = delegate_mfold.delay(data.upper())
    return jsonify({'task_id': resource.task_id})


@app.route('/designer/status/<task_id>')
def designer_task_status(task_id):
    return jsonify(get_async_result(
        design_and_score, task_id, only_status=True
    ))


@app.route('/designer/result/<task_id>')
def designer_task_result(task_id):
    return jsonify()


@app.route('/designer/<data>')
def design_handler(data):
    resource = design_and_score.delay(data.upper())
    return jsonify({'task_id': resource.task_id})
