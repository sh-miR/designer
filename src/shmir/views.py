"""
.. module:: views
    :synopsis: module to handle all urls of RESTful
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
    """Mfold status getter

    Args:
        task_id: Id of task generated via RESTful API

    Returns:
        Json object with status of specific id
    """
    return jsonify(get_async_result(delegate_mfold, task_id, only_status=True))


def mfold_zip(path, task_id):
    """Function to check if mfold task of given ID is done
        and sending the result in zip file

    Args:
        path: path where we look for folded structures
        task_id: Id of task generated via RESTful API

    Returns:
        Json object of status or sends zipped file
    """
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
    """Handler for getting mfold result from just a task id

    Args:
        task_id: Id of task generated via RESTful API

    Returns:
        Json object of status or sends zipped file
    """
    return mfold_zip(task_id, task_id)


@app.route('/mfold/result/<dir1>/<dir2>')
def mfold_from_subdirs(dir1, dir2):
    """Handler for getting mfold result from subdirectory and task id

    Args:
        dir1: subdirectory of given task
        dir2: Id of task generated via RESTful API (same as directory)

    Returns:
        Json object of status or sends zipped file
    """
    return mfold_zip("%s/%s" % (dir1, dir2), dir2)


@app.route('/mfold/<data>')
@cache.memoize()
def mfold_data_handler(data):
    """Handler to create folded structure via mfold for specific sequence.

    Args:
        data: sequence

    Returns:
        Task id of this task
    """
    resource = delegate_mfold.apply_async(args=(data.upper(),),
                                          kwargs=request.args.to_dict(),
                                          queue='score')
    return jsonify({'task_id': resource.task_id})


@app.route('/from_sirna/status/<task_id>')
def designer_task_status(task_id):
    """Handler to check status of task which creates sh-miR from siRNA

    Args:
        task_id: Id of task generated via RESTful API

    Returns:
        Json object with status of given task_id

    """
    return jsonify(get_async_result(
        shmir_from_sirna_score, task_id, only_status=True)
    )


@app.route('/from_sirna/result/<task_id>')
def designer_task_result(task_id):
    """Handler to give result of sh-miR(s) created from siRNA

    Args:
        task_id: Id of task generated via RESTful API

    Returns:
        Json object with sh-miRs created from siRNA:
        [(score, sh-miR, bacbone name, pdf(id to download pdf via mfold)...]
    """
    result = get_async_result(shmir_from_sirna_score, task_id)

    return jsonify(result)


@app.route('/from_sirna/<data>')
@cache.memoize()
def design_handler(data):
    """Handler to initialize task which creates sh-miR(s) from siRNA

    Args:
        data: one siRNA strand (active) or two siRNA strands separated by space.
            First strand is active, both are in 5-3 orientation.
    Returns:
        Task id
    """
    resource = shmir_from_sirna_score.apply_async(
        args=(data.upper(),), kwargs=request.args.to_dict(), queue='score')
    return jsonify({'task_id': resource.task_id})


@app.route('/from_transcript/status/<task_id>')
def transcript_task_status(task_id):
    """Handler to check status of task which creates sh-miR from transcript

    Args:
        task_id: Id of task generated via RESTful API

    Returns:
        Json object with status of given task_id

    """
    return jsonify(get_async_result(
        shmir_from_transcript_sequence, task_id, only_status=True)
    )


@app.route('/from_transcript/result/<task_id>')
def transcript_task_result(task_id):
    """Handler to get results of task which creates sh-miR(s) from transcript

    Args:
        task_id: Id of task generated via RESTful API
    Returns:
        Json object with list of sh-miRs in structure:
        [sh-miR, score, pdf(id to download pdf via mfold), sequence and backbone name...]
    """
    result = get_async_result(shmir_from_transcript_sequence, task_id)

    return jsonify(result)


@app.route('/from_transcript/<transcript_name>')
@cache.memoize()
def transcript_handler(transcript_name):
    """Handler to create sh-miR from transcript
    Args:
        transcript_name: name of transcript
    Returns:
        Id of task
    """
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
@cache.memoize()
def get_structures():
    """Handler to list all possible backbones
    Returns:
        Json object with names of backbones list
    """
    return jsonify({
        'templates': [
            columns[0] for columns in db_session.query(Backbone.name)]
    })
