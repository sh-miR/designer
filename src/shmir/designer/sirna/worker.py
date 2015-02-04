"""
.. module:: shmir.designer.sirna.worker
    :synopsis: provides worker to create sh-miR from siRNA
"""

from copy import deepcopy
from itertools import izip

from celery import group
from celery.result import allow_join_result
from shmir.async import task

from shmir.settings import SIRNA_RESULT_LIMIT

from shmir.result_handlers import zip_files_from_sirna
from shmir.decorators import (
    catch_errors,
    send_email
)

from shmir.designer.utils import adjusted_frames
from shmir.designer.mfold.worker import fold
from shmir.designer.sirna.score import score_from_sirna
from shmir.designer.errors import (
    NoResultError,
    ValidationError,
)

from shmir.data.db_api import frames_by_scaffold


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
            'sequences': (frame.siRNA1, frame.siRNA2),
        }
        for score, shmir, frame, folding in izip(scores, shmirs, frames, foldings)
        if score['all'] > 60
    ]

    return sorted(
        full_reference,
        key=lambda elem: elem['score']['all'],
        reverse=True
    )[:SIRNA_RESULT_LIMIT]
