"""
.. module:: main
    :synopsis: provides the executable program
"""

import operator
import json
from copy import deepcopy

from celery import group
from celery.result import allow_join_result

from .validators import check_input
from .utils import (
    get_frames,
    reverse_complement,
)
from shmir.designer.score import (
    score_frame,
    score_homogeneity,
    score_two_same_strands,
)
from shmir.designer.search import find_by_patterns
from shmir.async import task
from shmir.contextmanagers import mfold_path
from shmir.data.models import (
    Backbone,
    InputData,
    db_session,
)
from shmir.data import ncbi_api
from shmir.mfold import (
    execute_mfold,
    zipped_mfold
)
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql import func


@task(bind=True)
def fold_and_score(self, seq1, seq2, frame_tuple, original):
    path_id = self.request.id
    score = 0
    frame, insert1, insert2 = frame_tuple

    mfold_data = execute_mfold(
        path_id, frame.template(insert1, insert2), zip_file=False
    )

    if 'error' in mfold_data:
        return mfold_data

    pdf, ss = mfold_data
    score += score_frame(frame_tuple, ss, original)
    score += score_homogeneity(original)
    score += score_two_same_strands(seq1, original)

    with mfold_path(self.request.id) as tmp_dirname:
        zipped_mfold(self.request.id, [pdf, ss], tmp_dirname)

    return (
        score, frame.template(insert1, insert2), frame.name, path_id
    )


@task
def shmir_from_sirna_score(input_str):
    """
    Main function takes string input and returns the best results depending
    on scoring. Single result include sh-miR sequence,
    score and link to 2D structure from mfold program
    """

    sequence = check_input(input_str)
    seq1, seq2, shift_left, shift_right = sequence
    if not seq2:
        seq2 = reverse_complement(seq1)

    original_frames = db_session.query(Backbone).all()

    frames = get_frames(seq1, seq2,
                        shift_left, shift_right,
                        deepcopy(original_frames))

    with allow_join_result():
        frames_with_score = group([
            fold_and_score.s(seq1, seq2, frame_tuple, original).set(queue="subtasks")
            for frame_tuple, original in zip(frames, original_frames)
        ]).apply_async().get()

    sorted_frames = [
        elem for elem in sorted(
            frames_with_score, key=operator.itemgetter(0), reverse=True
        ) if elem[0] > 60
    ][:3]

    return {'result': sorted_frames}


@task
def shmir_from_transcript_sequence(transcript_name, minimum_CG, maximum_CG,
                                   scaffold, stimulatory_sequences):
    # check if results are in database
    try:
        stored_input = db_session.query(InputData).filter(
            func.lower(InputData.transcript_name) == transcript_name.lower(),
            InputData.minimum_CG == minimum_CG,
            InputData.maximum_CG == maximum_CG,
            func.lower(InputData.scaffold) == scaffold.lower(),
            func.lower(InputData.stimulatory_sequences) == stimulatory_sequences.lower()
        ).one()
    except NoResultFound:
        stored_input = None

    if stored_input:
        return [result.as_json() for result in stored_input.results]  # hope it works this way...

    mRNA = ncbi_api.get_mRNA(transcript_name)

    if scaffold == 'all':
        frames = db_session.query(Backbone).all()
    else:
        frames = db_session.query(Backbone).filter(
            func.lower(Backbone.name) == scaffold
        ).all()

    patterns = [json.loads(frame.regexp) for frame in frames]

    for sequenece in find_by_patterns(patterns, mRNA):
        pass
