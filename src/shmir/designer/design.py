"""
.. module:: shmir.designer.design
    :synopsis: provides the executable program
"""

import operator
import json
from copy import deepcopy

from itertools import chain
from collections import (
    defaultdict,
    OrderedDict
)

from celery import group
from celery.result import allow_join_result

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql import func

from shmir.designer.validators import (
    check_input,
    validate_sequence,
)
from shmir.designer.utils import (
    generator_is_empty,
    get_frames,
    reverse_complement,
    unpack_dict_to_list,
    remove_none,
)
from shmir.designer.score import (
    score_from_sirna,
    score_from_transcript,
)
from shmir.designer.search import (
    find_by_patterns,
    all_possible_sequences,
)
from shmir.designer.errors import (
    NoResultError,
    ValidationError,
    IncorrectDataError,
)
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
from shmir.utils import remove_bad_foldings
from shmir.decorators import (
    catch_errors,
    send_email
)
from shmir.result_handlers import (
    zip_files_from_sirna,
    zip_files_from_transcript
)


@task(bind=True)
@catch_errors(NoResultError)
def fold_and_score(
    self, seq1, seq2, frame_tuple, original, score_fun, args_fun, prefix=None
):
    """Function for scoring and folding sequnces.

    Args:
        seq1(str): First RNA sequence.
        seq2(str): Second RNA sequence.
        frame_tuple(tuple): Tuple with frame and inserts.
        orginal(Backbone): orginal Backbone model.
        score_fun(function): Scoring function.
        args_fun(tuple): Arguments for scoring function.

    Kwargs:
        prefix(str): prefix for mfold path (default None)

    Returns:
        tuple with score, sh-miR, name of Backbone, task id and sequences.
    """
    if prefix:
        path_id = "%s/%s" % (prefix, self.request.id)
    else:
        path_id = self.request.id

    frame, insert1, insert2 = frame_tuple

    mfold_data = execute_mfold(
        path_id, frame.template(insert1, insert2), zip_file=False
    )

    pdf, ss = mfold_data
    score = score_fun(frame_tuple, original, ss, *args_fun)

    with mfold_path(path_id) as tmp_dirname:
        zipped_mfold(self.request.id, [pdf, ss], tmp_dirname)

    return [
        score,
        frame.template(insert1, insert2),
        frame.name,
        path_id,
        (seq1, seq2),
    ]


@task
@catch_errors(ValidationError, NoResultError)
@send_email(file_handler=zip_files_from_sirna)
def shmir_from_sirna_score(input_str):
    """Main function takes string input and returns the best results depending
    on scoring. Single result include sh-miR sequence,
    score and link to 2D structure from mfold program

    Args:
        input_str(str): Input string contains one or two sequences.

    Returns:
        List of sh-miR(s) sorted by score.
    """

    seq1, seq2, shift_left, shift_right = check_input(input_str)
    if not seq2:
        seq2 = reverse_complement(seq1)

    original_frames = db_session.query(Backbone).all()

    frames = get_frames(seq1, seq2,
                        shift_left, shift_right,
                        deepcopy(original_frames))

    with allow_join_result():
        frames_with_score = group(
            fold_and_score.s(
                seq1, seq2,
                frame_tuple,
                original,
                score_from_sirna,
                (seq1,)
            ).set(queue="subtasks")
            for frame_tuple, original in zip(frames, original_frames)
        ).apply_async().get()

    sorted_frames = [
        elem[:-1] for elem in sorted(
            frames_with_score, key=operator.itemgetter(0), reverse=True
        ) if elem[0] > 60
    ][:3]

    return sorted_frames


@task
def shmir_from_fasta_string(fasta_string, original_frames,
                            actual_offtarget, regexp_type, path):
    """Generating function of shmir from fasta string.

    Args:
        fasta_string(str): Sequence.
        original_frames(Backbone): original Backbone object.
        actual_offtarget(int): offtarget value
        regexp_type(int): Number of a regex from database.

    Returns:
        list of sh-miR(s)
    """
    seq2 = reverse_complement(fasta_string)

    frames = get_frames(fasta_string, seq2, 0, 0, deepcopy(original_frames))

    with allow_join_result():
        frames_with_score = group(
            fold_and_score.s(
                fasta_string,
                seq2,
                frame_tuple,
                original,
                score_from_transcript,
                (actual_offtarget, regexp_type),
                path
            ).set(queue="subtasks")
            for frame_tuple, original in zip(frames, original_frames)
        ).apply_async().get()

    filtered_frames = []
    for frame in frames_with_score:
        notes = frame[0]
        if notes['frame'] > 60 and notes['all'] > 100:
            frame[0] = notes['all']
            filtered_frames.append(frame)

    return sorted(filtered_frames, key=operator.itemgetter(0), reverse=True) or None


@task(bind=True, max_retries=10)
def validate_and_offtarget(self, sequence, maximum_offtarget, minimum_CG,
                           maximum_CG, stimulatory_sequences, regexp_type):
    """Function for validation and checking the target of sequence.
    Args:
        sequence(str): RNA sequence.
        maximum_offtarget(int): Maximum offtarget.
        minimum_CG(int): Minimum number of 'C' and 'G' nucleotide in sequence.
        maximum_CG(int): Maximum number of 'C' and 'G' nucleotide in sequence.
        stimulatory_sequences(str): One of 'yes', 'no', 'no_difference'.
        regexp_type(int): Number of a regex from database.

    Returns:
        If dict of sequence, regexp and offtarget value if is validated else None

    Raises:
        ValueError.

    """
    try:
        validated, actual_offtarget = validate_sequence(
            sequence, maximum_offtarget, minimum_CG,
            maximum_CG, stimulatory_sequences
        )
    except ValueError as exc:
        raise self.retry(exc=exc)

    if validated:
        return {
            'sequence': sequence,
            'regexp': regexp_type,
            'offtarget': actual_offtarget
        }


@task
@catch_errors(IncorrectDataError, NoResultError)
@send_email(file_handler=zip_files_from_transcript)
def shmir_from_transcript_sequence(
    transcript_name, minimum_CG, maximum_CG, maximum_offtarget, scaffold,
    stimulatory_sequences
):
    """Generating function of shmir from transcript sequence.
    Args:
        transcript_name(str): Name of transcipt.
        minimum_CG(int): Minimum number of 'C' and 'G' nucleotide in sequence.
        maximum_CG(int): Maximum number of 'C' and 'G' nucleotide in sequence.
        maximum_offtarget(int): Maximum offtarget.
        scaffold(str): Name of frame of miRNA or 'all'.
        stimulatory_sequences(str): One of 'yes', 'no', 'no_difference'.

    Returns:
        list of sh-miR(s).
    """
    # check if results are in database
    try:
        stored_input = db_session.query(InputData).filter(
            func.lower(InputData.transcript_name) == transcript_name.lower(),
            InputData.minimum_CG == minimum_CG,
            InputData.maximum_CG == maximum_CG,
            InputData.maximum_offtarget == maximum_offtarget,
            func.lower(InputData.scaffold) == scaffold.lower(),
            func.lower(
                InputData.stimulatory_sequences
            ) == stimulatory_sequences.lower()
        ).outerjoin(InputData.results).one()
    except NoResultFound:
        pass
    else:
        return [result.as_json() for result in stored_input.results]

    # create path string
    path = "_".join(
        map(
            str,
            [transcript_name, minimum_CG, maximum_CG, maximum_offtarget,
             scaffold, stimulatory_sequences]
        )
    )

    mRNA = ncbi_api.get_mRNA(transcript_name)

    if scaffold == 'all':
        original_frames = db_session.query(Backbone).all()
    else:
        original_frames = db_session.query(Backbone).filter(
            func.lower(Backbone.name) == scaffold.lower()
        ).all()

    frames_by_name = {frame.name: frame for frame in original_frames}

    patterns = {
        frame.name: OrderedDict(
            sorted(
                json.loads(frame.regexp).items(),
                reverse=True
            )
        ) for frame in original_frames
    }

    best_sequences = defaultdict(list)

    for name, patterns_dict in patterns.iteritems():
        for regexp_type, sequences in find_by_patterns(patterns_dict, mRNA).iteritems():
            with allow_join_result():
                is_empty, sequences = generator_is_empty(sequences)
                if not is_empty:
                    best_sequences[name] = remove_none(
                        group(
                            validate_and_offtarget.s(
                                sequence,
                                maximum_offtarget,
                                minimum_CG,
                                maximum_CG,
                                stimulatory_sequences,
                                int(regexp_type)
                            ).set(queue="blast")
                            for sequence in sequences
                        ).apply_async().get()
                    )

    results = []
    for name, seq_dict in unpack_dict_to_list(best_sequences):
        if len(results) == 20:
            break
        with allow_join_result():
            shmir_result = shmir_from_fasta_string.s(
                seq_dict['sequence'],
                [frames_by_name[name]],
                seq_dict['offtarget'],
                seq_dict['regexp'],
                path
            ).set(queue="score").apply_async().get()

            if shmir_result:
                results.extend(shmir_result)

    if not results:
        best_sequences = []
        sequences = all_possible_sequences(mRNA, 19, 21)

        with allow_join_result():
            is_empty, sequences = generator_is_empty(sequences)
            if not is_empty:
                best_sequences = remove_none(
                    group(
                        validate_and_offtarget.s(
                            sequence,
                            maximum_offtarget,
                            minimum_CG,
                            maximum_CG,
                            stimulatory_sequences,
                            0
                        ).set(queue="blast")
                        for sequence in sequences
                    ).apply_async().get()
                )

        if best_sequences:
            with allow_join_result():
                results = chain(*remove_none(
                    group(
                        shmir_from_fasta_string.s(
                            seq_dict['sequence'], original_frames,
                            seq_dict['offtarget'], seq_dict['regexp'], path
                        ).set(queue="score")
                        for seq_dict in best_sequences
                    ).apply_async().get()
                ))

    sorted_results = sorted(
        results,
        key=operator.itemgetter(0),
        reverse=True
    )[:10]
    db_results = [Result(
        score=score,
        sh_mir=shmir,
        pdf=path_id,
        backbone=frames_by_name[frame_name].id,
        sequence=found_sequences[0],
    ) for score, shmir, frame_name, path_id, found_sequences in sorted_results]

    remove_bad_foldings(path, (result.get_task_id() for result in db_results))

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

    return [result.as_json() for result in db_results]
