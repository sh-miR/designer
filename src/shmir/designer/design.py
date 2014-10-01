"""
.. module:: main
    :synopsis: provides the executable program
"""

import operator
import json
import math
from copy import deepcopy

from collections import defaultdict
from itertools import chain

from celery import group
from celery.result import allow_join_result

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql import func

from shmir.designer.validators import check_input
from shmir.designer.utils import (
    get_frames,
    reverse_complement,
)
from shmir.designer.score import (
    score_from_sirna,
    score_from_transcript,
)
from shmir.designer.search import find_by_patterns
from shmir.designer.validators import validate_gc_content
from shmir.designer.offtarget import check_offtarget
from shmir.async import task
from shmir.contextmanagers import mfold_path
from shmir.data.models import (
    Backbone,
    Immuno,
    InputData,
    db_session,
)
from shmir.data import ncbi_api
from shmir.mfold import (
    execute_mfold,
    zipped_mfold
)


@task(bind=True)
def fold_and_score(self, seq1, seq2, frame_tuple, original, score_fun):
    path_id = self.request.id
    frame, insert1, insert2 = frame_tuple

    mfold_data = execute_mfold(
        path_id, frame.template(insert1, insert2), zip_file=False
    )

    if 'error' in mfold_data:
        return mfold_data

    pdf, ss = mfold_data
    score = score_fun(frame_tuple, original,  seq1, ss)

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

    seq1, seq2, shift_left, shift_right = check_input(input_str)
    if not seq2:
        seq2 = reverse_complement(seq1)

    original_frames = db_session.query(Backbone).all()

    frames = get_frames(seq1, seq2,
                        shift_left, shift_right,
                        deepcopy(original_frames))

    with allow_join_result():
        frames_with_score = group([
            fold_and_score.s(seq1, seq2, frame_tuple,
                             original, score_from_sirna).set(queue="subtasks")
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
                                   maximum_offtarget, scaffold, stimulatory_sequences):
    # check if results are in database
    try:
        stored_input = db_session.query(InputData).filter(
            func.lower(InputData.transcript_name) == transcript_name.lower(),
            InputData.minimum_CG == minimum_CG,
            InputData.maximum_CG == maximum_CG,
            InputData.maximum_offtarget == maximum_offtarget,
            func.lower(InputData.scaffold) == scaffold.lower(),
            func.lower(InputData.stimulatory_sequences) == stimulatory_sequences.lower()
        ).one()
    except NoResultFound:
        stored_input = None

    if stored_input:
        return [result.as_json() for result in stored_input.results]  # hope it works this way...

    mRNA = ncbi_api.get_mRNA(transcript_name)

    if scaffold == 'all':
        frames = db_session.query(Backbone.name, Backbone.regexp).all()
    else:
        frames = db_session.query(Backbone.name, Backbone.regexp).filter(
            func.lower(Backbone.name) == scaffold
        ).all()

    patterns = {frame[0]: json.loads(frame[1]) for frame in frames}
    best_sequeneces = defaultdict(list)

    for name, patterns_dict in patterns.items():
        for sequence in chain(*find_by_patterns(patterns_dict, mRNA).itervalues()):

            if len(best_sequeneces[name]) > math.ceil(10. / len(frames)):
                break

            if (validate_gc_content(sequence, minimum_CG, maximum_CG) and
               check_offtarget(sequence, maximum_offtarget)):
                if stimulatory_sequences == 'no_difference':
                    best_sequeneces[name].append(sequence)
                else:
                    is_immuno = Immuno.check_is_in_sequence(sequence)
                    if is_immuno and stimulatory_sequences == 'yes':
                        best_sequeneces[name].append(sequence)
                    elif not is_immuno and stimulatory_sequences == 'no':
                        best_sequeneces[name].append(sequence)
