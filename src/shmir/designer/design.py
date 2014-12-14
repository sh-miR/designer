"""
.. module:: shmir.designer.design
    :synopsis: provides the executable program
"""

import operator
import json
from copy import deepcopy

from itertools import (
    chain,
    ifilter,
)
from collections import (
    defaultdict,
    OrderedDict
)

from celery import group
from celery.result import allow_join_result

from shmir.designer.validators import (
    parse_input,
    validate_sequence,
    validate_gc_content,
    validate_immuno,
)
from shmir.designer.utils import (
    generator_is_empty,
    adjusted_frames,
    reverse_complement,
    unpack_dict_to_list,
    remove_none,
    create_path_string,
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
from shmir.data.db_api import (
    get_results,
    frames_by_scaffold,
)
from shmir import mfold
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

    mfold_data = mfold.execute(
        path_id, frame.template(insert1, insert2), to_zip=False
    )

    pdf, ss = mfold_data
    score = score_fun(frame_tuple, original, ss, *args_fun)

    with mfold_path(path_id) as tmp_dirname:
        mfold.zip_file(self.request.id, [pdf, ss], tmp_dirname)

    return [
        score,
        frame.template(insert1, insert2),
        frame.name,
        path_id,
        (seq1, seq2),
    ]


@task(bind=True)
def fold(self, shmiR):
    task_id = self.request.id
    pdf, ss = mfold.execute(
        task_id, shmiR, to_zip=False
    )
    with mfold_path(task_id) as tmp_dirname:
        mfold.zip_file(task_id, [pdf, ss], tmp_dirname)

    return {
        'task_id': task_id,
        'ss': ss,
    }


@task
@catch_errors(ValidationError, NoResultError)
@send_email(file_handler=zip_files_from_sirna)
def shmir_from_sirna_score(seq1, seq2, shift_left, shift_right):
    """Main function takes string input and returns the best results depending
    on scoring. Single result include sh-miR sequence,
    score and link to 2D structure from mfold program

    Args:
        input_str(str): Input string contains one or two sequences.

    Returns:
        List of sh-miR(s) sorted by score.
    """
    original_frames = db_session.query(Backbone).all()

    frames = adjusted_frames(seq1, seq2,
                             shift_left, shift_right,
                             deepcopy(original_frames))

    shmirs = [frame.template() for frame in frames]

    # folding via mfold
    with allow_join_result():
        foldings = group(
            fold.s(
                shmir
            ).set(queue="subtasks") for shmir in shmirs
        ).apply_async().get()

    # scoring results
    with allow_join_result():
        scores = group(
            score_from_sirna.s(
                frame,
                original,
                folding['ss']
            ).set(queue="subtasks")
            for frame, original, folding in zip(frames, original_frames, foldings)
        ).apply_async().get()

    full_reference = [
        {
            'score': score,
            'shmir': shmir,
            'scaffold_name': frame.name,
            'pdf_reference': folding['task_id'],
            'scaffolds': (frame.siRNA1, frame.siRNA2),
        }
        for score, shmir, frame, folding in zip(scores, shmirs, frames, foldings)
        if score['all'] > 60
    ]

    return sorted(
        full_reference,
        key=lambda elem: elem['score']['all'],
        reverse=True
    )[:3]


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

    frames = adjusted_frames(fasta_string, seq2, 0, 0, deepcopy(original_frames))

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
def validate_sequences(
    sequences, regexp, name,
    minimum_CG, maximum_CG, maximum_offtarget, immuno
):
    """
    Here we remove all bad sequences (siRNA) by validators
    """

    # filter sequences here by no expensive features
    preprocessed = filter(
        lambda sequence:
        all([
            validate_gc_content(
                sequence,
                minimum_CG,
                maximum_CG
            ),
            validate_immuno(
                sequence,
                immuno
            )]),
        sequences
    )
    # uncomment if debuging
    return {
        name: [{
            "sequence": seq,
            "regexp": int(regexp),
            "offtarget": 0}
            for seq in preprocessed]
    }

    # counting offtarget is expensive
    with allow_join_result():
        offtarget = group(
            blast_offtarget.s(
                sequence,
            ).set(queue="blast")
            for sequence in preprocessed
        ).apply_async().get()

    return {
        name: [{
            "sequence": sequence,
            "regexp": int(regexp),
            "offtarget": actual_offtarget}

            for sequence, actual_offtarget
            in zip(preprocessed, offtarget)
            if actual_offtarget <= maximum_offtarget]
    }


@task
@catch_errors(IncorrectDataError, NoResultError)
@send_email(file_handler=zip_files_from_transcript)
def shmir_from_transcript_sequence(
    transcript_name, minimum_CG, maximum_CG, maximum_offtarget, scaffold,
    immunostimulatory
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
    results = get_results(
        transcript_name,
        minimum_CG,
        maximum_CG,
        maximum_offtarget,
        scaffold,
        immunostimulatory
    )

    # sometimes results is an empty list
    if results is not None:
        return results

    path = create_path_string(
        transcript_name,
        minimum_CG,
        maximum_CG,
        maximum_offtarget,
        scaffold,
        immunostimulatory
    )

    mRNA = ncbi_api.get_mRNA(transcript_name)

    original_frames = frames_by_scaffold(scaffold)

    frames_by_name = {frame.name: frame for frame in original_frames}

    # best patters should be choosen first
    patterns = {
        frame.name: OrderedDict(
            sorted(
                json.loads(frame.regexp).items(),
                reverse=True
            )
        ) for frame in original_frames
    }

    with allow_join_result():
        validated = group(
            validate_sequences.s(
                list(sequences),  # generators are not serializable
                regexp_type,
                name,
                minimum_CG,
                maximum_CG,
                maximum_offtarget,
                immunostimulatory).set(queue="score")

            for name, patterns_dict in patterns.iteritems()
            for regexp_type, sequences
            in find_by_patterns(patterns_dict, mRNA).iteritems()

            ).apply_async().get()

    # merge results by name
    best_sequences = defaultdict(list)
    for valid_group in validated:
        for name, sequences in valid_group.iteritems():
            best_sequences[name].append(sequences)

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
                            immunostimulatory,
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
        stimulatory_sequences=immunostimulatory,
        results=db_results
    )
    db_session.add(db_input)
    db_session.add_all(db_results)
    db_session.commit()

    return [result.as_json() for result in db_results]
