"""
.. module:: main
    :synopsis: provides the executable program
"""

import operator
import json
from copy import deepcopy

from collections import defaultdict

from celery import group
from celery.result import allow_join_result
from celery.utils.log import get_task_logger

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql import func

from shmir.designer.validators import (
    check_input,
    validate_sequence,
)
from shmir.designer.utils import (
    get_frames,
    reverse_complement,
    unpack_dict_to_list,
)
from shmir.designer.score import (
    score_from_sirna,
    score_from_transcript,
)
from shmir.designer.search import (
    find_by_patterns,
    all_possible_sequences,
)
from shmir.designer.offtarget import blast_offtarget
from shmir.async import task
from shmir.contextmanagers import mfold_path
from shmir.data.models import (
    Backbone,
    InputData,
    Result,
    db_session,
)
from shmir.data import ncbi_api
from shmir.mfold import (
    execute_mfold,
    zipped_mfold
)


logger = get_task_logger(__name__)


@task(bind=True)
def fold_and_score(self, seq1, seq2, frame_tuple, original, score_fun, args_fun):
    path_id = self.request.id
    frame, insert1, insert2 = frame_tuple

    mfold_data = execute_mfold(
        path_id, frame.template(insert1, insert2), zip_file=False
    )

    if 'error' in mfold_data:
        return mfold_data

    pdf, ss = mfold_data
    score = score_fun(frame_tuple, original, ss, *args_fun)

    with mfold_path(self.request.id) as tmp_dirname:
        zipped_mfold(self.request.id, [pdf, ss], tmp_dirname)

    return (
        score, frame.template(insert1, insert2), frame.name, path_id, (seq1, seq2),
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
                             original, score_from_sirna,
                             (seq1,)).set(queue="subtasks")
            for frame_tuple, original in zip(frames, original_frames)
        ]).apply_async().get()

    sorted_frames = [
        elem[:-1] for elem in sorted(
            frames_with_score, key=operator.itemgetter(0), reverse=True
        ) if elem[0] > 60
    ][:3]

    return sorted_frames


@task
def shmir_from_fasta_string(fasta_string, original_frames,
                            actual_offtarget, regexp_type):
    seq2 = reverse_complement(fasta_string)

    frames = get_frames(fasta_string, seq2, 0, 0, deepcopy(original_frames))

    with allow_join_result():
        frames_with_score = group([
            fold_and_score.s(fasta_string, seq2, frame_tuple,
                             original, score_from_transcript,
                             (actual_offtarget, regexp_type)
                             ).set(queue="subtasks")
            for frame_tuple, original in zip(frames, original_frames)
        ]).apply_async().get()

    filtered_frames = []
    for frame in frames_with_score:
        notes = frame[0]
        if notes['frame'] > 60 and notes['all'] > 100:
            frame[0] = notes['all']
            filtered_frames.append(frame)

    return sorted(filtered_frames, key=operator.itemgetter(0), reverse=True)


@task
def shmir_from_transcript_sequence(transcript_name, minimum_CG, maximum_CG,
                                   maximum_offtarget, scaffold, stimulatory_sequences):
    # check if results are in database
    logger.info('Checking whether results are in database')
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
        pass
    else:
        return [result.as_json() for result in stored_input.results]

    logger.info('Checked results in database')
    logger.info('Getting data from NCBI')

    mRNA = ncbi_api.get_mRNA(transcript_name)[400]

    logger.info('Got data from NCBI')
    logger.info('Getting original frames')

    if scaffold == 'all':
        original_frames = db_session.query(Backbone).all()
    else:
        original_frames = db_session.query(Backbone).filter(
            func.lower(Backbone.name) == scaffold
        ).all()

    frames_by_name = {frame.name: [frame] for frame in original_frames}

    patterns = {frame.name: json.loads(frame.regexp) for frame in original_frames}
    best_sequeneces = defaultdict(list)

    logger.info('Got original frames')
    logger.info('Processing patterns')

    for name, patterns_dict in patterns.iteritems():
        for regexp_type, sequences in find_by_patterns(patterns_dict, mRNA).iteritems():
            for sequence in sequences:

                actual_offtarget = blast_offtarget(sequence)
                if validate_sequence(sequence, actual_offtarget, maximum_offtarget,
                                     minimum_CG, maximum_CG, stimulatory_sequences):
                    best_sequeneces[name].append({
                        'sequence': sequence,
                        'regexp': regexp_type,
                        'offtarget': actual_offtarget
                    })

    logger.info('Patterns processed')
    logger.info('Unpacking structures')

    results = []
    for name, seq_dict in unpack_dict_to_list(best_sequeneces):
        if len(results) == 10:
            break
        with allow_join_result():
            results.extend(shmir_from_fasta_string.s(
                seq_dict['sequence'], frames_by_name[name],
                seq_dict['offtarget'], seq_dict['regexp']
            ).set(queue="score").apply_async().get())

    logger.info('Sctructures unpacked')
    logger.info('Getting best sequences, offtarget')

    if not results:
        best_sequeneces = []
        for sequence in all_possible_sequences(mRNA, 19, 21):
            actual_offtarget = blast_offtarget(sequence)
            if validate_sequence(sequence, actual_offtarget, maximum_offtarget,
                                 minimum_CG, maximum_CG, stimulatory_sequences):
                best_sequeneces.append({
                    'sequence': sequence,
                    'regexp': 0,
                    'offtarget': actual_offtarget
                })

        logger.info('best seqs: %r', best_sequeneces)
        logger.info('sqs len: %d', len(best_sequeneces))

        if best_sequeneces != []:
            with allow_join_result():
                results = group([
                    shmir_from_fasta_string.s(seq_dict['sequence'], original_frames,
                                            seq_dict['offtarget'], seq_dict['regexp']
                                            ).set(queue="score")
                    for seq_dict in best_sequeneces]).apply_async().get()

    logger.info('Got best sequences, offtarget calculated')
    logger.info('Storing DB results')

    sorted_results = sorted(results, key=operator.itemgetter(0), reverse=True)[:5]
    db_results = [Result(
        score=score,
        sh_mir=shmir,
        pdf=path_id,
        backbone=frames_by_name[frame_name],
        sequence=sequences[0],
    ) for score, shmir, frame_name, path_id, sequencess in sorted_results]

    db_input = InputData(
        transcript_name=transcript_name,
        minimum_CG=minimum_CG,
        maximum_CG=maximum_CG,
        maximum_offtarget=maximum_offtarget,
        scaffold=scaffold,
        stimulatory_sequences=stimulatory_sequences,
        results=db_results
    )
    db_session.add(db_input)
    db_session.add_all(db_results)
    db_session.commit()

    logger.info('DB results stored')
    logger.info('End of task')

    return [result.as_json() for result in db_results]
