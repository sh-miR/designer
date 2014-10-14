"""
Handlers

"""

from flask import (
    jsonify,
    request,
    send_file
)

from shmir import (
    app,
    cache
)
from shmir.async import get_async_result
from shmir.designer.design import (
    shmir_from_sirna_score,
    shmir_from_transcript_sequence
)
from shmir.mfold import delegate_mfold
from shmir.utils import get_zip_path
from data.models import (
    Backbone,
    db_session,
)


@app.route('/mfold/status/<task_id>')
def mfold_task_status(task_id):
    return jsonify(get_async_result(delegate_mfold, task_id, only_status=True))


def mfold_zip(path, task_id):
    status = get_async_result(delegate_mfold, task_id)
    if status['status'] == 'fail':
        return jsonify({
            'status': 'error', 'error': 'Task is not ready or has failed'
        })
    elif status['status'] == 'error':
        return jsonify(status)

    zip_file = get_zip_path(path, task_id)
    try:
        return send_file(zip_file)
    except IOError:
        return jsonify({
            'status': 'error', 'error': 'File does not exist'
        })


@app.route('/mfold/result/<task_id>')
def mfold_from_subdir(task_id):
    return mfold_zip(task_id, task_id)


@app.route('/mfold/result/<dir1>/<dir2>')
def mfold_from_subdirs(dir1, dir2):
    return mfold_zip("%s/%s" % (dir1, dir2), dir2)


@app.route('/mfold/<data>')
@cache.cached()
def mfold_data_handler(data):
    resource = delegate_mfold.apply_async(args=(data.upper(),),
                                          kwargs=request.args.to_dict(),
                                          queue='score')
    return jsonify({'task_id': resource.task_id})


@app.route('/from_sirna/status/<task_id>')
def designer_task_status(task_id):
    return jsonify(get_async_result(
        shmir_from_sirna_score, task_id, only_status=True)
    )


@app.route('/from_sirna/result/<task_id>')
def designer_task_result(task_id):
    result = get_async_result(shmir_from_sirna_score, task_id)

    return jsonify(result)


@app.route('/from_sirna/<data>')
@cache.cached()
def design_handler(data):
    resource = shmir_from_sirna_score.apply_async(
        args=(data.upper(),), kwargs=request.args.to_dict(), queue='score')
    return jsonify({'task_id': resource.task_id})


@app.route('/from_transcript/status/<task_id>')
def transcript_task_status(task_id):
    return jsonify(get_async_result(
        shmir_from_transcript_sequence, task_id, only_status=True)
    )


@app.route('/from_transcript/result/<task_id>')
def transcript_task_result(task_id):
    result = get_async_result(shmir_from_transcript_sequence, task_id)

    return jsonify(result)


@app.route('/from_transcript/<transcript_name>')
@cache.cached()
def transcript_handler(transcript_name):
    params = (
        ('min_gc', 40, int),
        ('max_gc', 60, int),
        ('max_offtarget', 10, int),
        ('mirna_name', 'all', str),
        ('stymulators', 'no_difference', str)
    )
    args = tuple([transcript_name] + [
        param_type(request.args.get(key, default))
        for key, default, param_type in params
    ])

    resource = shmir_from_transcript_sequence.apply_async(args=args,
                                                          queue='design')

    return jsonify({'task_id': resource.task_id})


@app.route('/structures')
def get_structures():
    return jsonify({
        'templates': [
            columns[0] for columns in db_session.query(Backbone.name)]
    })
