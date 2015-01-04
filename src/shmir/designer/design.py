"""
.. module:: shmir.designer.design
    :synopsis: provides the executable program
"""

import json
from copy import deepcopy

from itertools import (
    chain,
    izip,
)
from collections import (
    OrderedDict,
)

from celery import group
from celery.result import allow_join_result

from shmir.designer.validators import (
    validate_gc_content,
    validate_immuno,
    validate_transcript_by_score,
)
from shmir.designer.utils import (
    adjusted_frames,
    reverse_complement,
    unpack_dict_to_list,
    create_path_string,
    merge_results,
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
from shmir.data import ncbi_api
from shmir.data.db_api import (
    get_results,
    frames_by_scaffold,
    store_results,
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
from shmir.settings import TRANSCRIPT_RESULT_LIMIT


@task(bind=True)
def fold(self, shmiR, prefix=None):
    task_id = self.request.id

    if prefix is not None:
        task_id = "{}/{}".format(prefix, task_id)

    pdf, ss = mfold.execute(
        task_id, shmiR, to_zip=False
    )
    with mfold_path(task_id) as tmp_dirname:
        mfold.zip_file(self.request.id, [pdf, ss], tmp_dirname)

    return {
        'path_id': task_id,
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
    original_frames = frames_by_scaffold('all')

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
            for frame, original, folding in izip(frames, original_frames, foldings)
        ).apply_async().get()

    full_reference = [
        {
            'score': score,
            'shmir': shmir,
            'scaffold_name': frame.name,
            'pdf_reference': folding['path_id'],
            'scaffolds': (frame.siRNA1, frame.siRNA2),
        }
        for score, shmir, frame, folding in izip(scores, shmirs, frames, foldings)
        if score['all'] > 60
    ]

    return sorted(
        full_reference,
        key=lambda elem: elem['score']['all'],
        reverse=True
    )[:3]


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
    # return {
    #     name: [{
    #         "sequence": seq,
    #         "regexp": int(regexp),
    #         "offtarget": 0}
    #         for seq in preprocessed]
    # }

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
            in izip(preprocessed, offtarget)
            if actual_offtarget <= maximum_offtarget]
    }


@task
def shmir_from_fasta(siRNA, offtarget, regexp, original_frames, prefix):
    siRNA2 = reverse_complement(siRNA)

    frames = adjusted_frames(
        siRNA,
        siRNA2,
        0, 0,  # we do not have shifts here
        deepcopy(original_frames)
    )

    shmirs = [frame.template() for frame in frames]

    with allow_join_result():
        foldings = group(
            fold.s(
                shmir,
                prefix=prefix
            ).set(queue="subtasks")
            for shmir in shmirs
        ).apply_async().get()

    results = []
    for frame, original_frame, folding in izip(frames, original_frames, foldings):
        score = score_from_transcript(
            frame,
            original_frame,
            folding['ss'],
            offtarget,
            regexp,
        )
        if validate_transcript_by_score(score):
            results.append({
                "score": score,
                "frame": frame,
                "folding": folding,
                "found_sequence": siRNA,
            })
    return results


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
    reversed_mRNA = reverse_complement(mRNA)

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
            in find_by_patterns(patterns_dict, reversed_mRNA).iteritems()

        ).apply_async().get()

    best_sequences = merge_results(validated)

    with allow_join_result():
        results = group(
            shmir_from_fasta.s(
                siRNA['sequence'],
                siRNA['offtarget'],
                siRNA['regexp'],
                [frames_by_name[name]],
                path,
            ).set(queue="score")
            for name, siRNA in unpack_dict_to_list(best_sequences)
        ).apply_async().get()

    # merge
    results = list(chain(*results))

    if not results:
        with allow_join_result():
            validated = validate_sequences.s(
                list(all_possible_sequences(reversed_mRNA, 21)),  # not serializable
                0,
                'all',
                minimum_CG,
                maximum_CG,
                maximum_offtarget,
                immunostimulatory
            ).apply_async(queue="subtasks").get()
        best_sequences = merge_results([validated])

        with allow_join_result():
            results = group(
                shmir_from_fasta.s(
                    siRNA['sequence'],
                    siRNA['offtarget'],
                    siRNA['regexp'],
                    original_frames,
                    path
                ).set(queue="score")
                for name, siRNA in unpack_dict_to_list(best_sequences)
            ).apply_async().get()

        # merge
        results = chain(*results)

    sorted_results = sorted(
        results,
        key=lambda result: result['score']['all'],
        reverse=True
    )[:TRANSCRIPT_RESULT_LIMIT]

    db_results = store_results(
        transcript_name,
        minimum_CG,
        maximum_CG,
        maximum_offtarget,
        scaffold,
        immunostimulatory,
        sorted_results,
    )

    remove_bad_foldings(path, (result.get_task_id() for result in db_results))

    return [result.as_json() for result in db_results]
