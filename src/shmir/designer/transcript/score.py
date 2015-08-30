"""
.. module:: score
    :synopsis: This module provides scoring sh-miRs created from transcript
"""

from shmir.designer.mfold.score import score_structure


def score_offtarget(number):
    """Function counts score.

    Args:
        number: Count of founded offtargets.

    Returns:
        score(int): Number from 0 to 40, depending on offtarget.
    """
    score = 40 - number * 2
    if score >= 0:
        return score
    return 0


def score_regexp(number):
    """Function which gives score for regexp of found sequence

    Args:
        number(int): regexp number from database.

    Returns
        score(int): regexp * 5.
    """
    return number * 5


def score_thermostability(
    frame
):
    """Function to scores thermostability of siRNA.

        Args:
        seq1(str): First RNA sequence.
        seq2(str): Second RNA sequence.

        Returns: Tuple with:
        Thermostability score(int), where 0 means discard,
        1 means somehow efficient,
        2 means efficient.
    """
    if frame.siRNA2[0] == 'G' and (frame.siRNA2[:-1] == 'A' or frame.siRNA2[:-1] == 'T'):
        thermostability_score = 20
    elif (frame.siRNA2[0] == 'C' and
          (frame.siRNA2[:-1] == 'A' or frame.siRNA2[:-1] == 'T')):
        thermostability_score = 15
    elif (frame.siRNA2[0] == 'A' or frame.siRNA2[0] == 'T' and
          (frame.siRNA2[:-1] == 'A' or frame.siRNA2[:-1] == 'T')):
        thermostability_score = 5
    return thermostability_score


def score_from_transcript(
    frame, original_frame, frame_ss, offtarget, regexp
):
    """
    Function which count score from transcript.

    Args:
        frame: backbone object
        original_frame: sh-miR object
        frame_ss: file from mfold
        offtarget: Number of transcripts
        regexp: Number of regular expression

    Returns:
        Dict of scores for: frame, offtarget, regexp and all together.
    """
    structure_points = score_structure(frame, frame_ss, original_frame)
    offtarget_points = score_offtarget(offtarget)
    regexp_points = score_regexp(regexp)
    thermostability_points = score_thermostability(frame)
    return {
        'structure': structure_points,
        'offtarget': offtarget_points,
        'regexp': regexp_points,
        'thermostability': thermostability_points,
        'all': (
            structure_points + offtarget_points +
            regexp_points + thermostability_points
        )
    }
