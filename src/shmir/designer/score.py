"""
.. module:: score
    :synopsis: This module provides scroing frames.
"""

from math import ceil
from .ss import parse_ss
from .ss import parse_score
from shmir.async import task


def score_structure(frame, folding_file, original_frame):
    """Scorring function.

    Args:
        frame: Backbone object with added siRNAs
        folding_file: file from mfold
        ss_file: object Backbone from database (not changed)

    Returns:
        score(int): score given for structure of frame.
    """

    structure_ss = parse_ss(folding_file)
    max_score, orginal_score = parse_score(original_frame.structure)

    # differences
    flanks5 = len(original_frame.flanks5_s) - len(frame.flanks5_s)
    insertion1 = len(original_frame.miRNA_s) - len(frame.siRNA1)
    loop = len(original_frame.loop_s) - len(frame.loop_s)
    insertion2 = len(original_frame.miRNA_a) - len(frame.siRNA2)
    flanks3 = len(original_frame.flanks3_s) - len(frame.flanks3_s)

    position = len(frame.flanks5_s)  # position in sequence (list)
    structure_len = len(frame.template())
    current = position + flanks5  # current position (after changes)

    if flanks5 < 0:
        add_shifts(0, structure_len, structure_ss, flanks5, 0)
    else:
        add_shifts(position, structure_len,
                   structure_ss, flanks5, current)
    for diff, nucleotides in [(insertion1, frame.siRNA1), (loop, frame.loop_s),
                              (insertion2, frame.siRNA2), (flanks3, '')]:
        position += len(nucleotides)
        current = position + diff
        add_shifts(position, structure_len, structure_ss, diff, current)
    score = 0
    for created in structure_ss:
        for orginal, points in orginal_score:
            if created == orginal:
                score += points
    return int(ceil(score/max_score * 100))


def add_shifts(start, end, fold_ss, value, current):
    """The numbers assigned to the nucleotides have to be verified,
    because flanking sequences can be shortened or extended during insertion.
    Moreover, the length of the siRNA insert can differ from the natural one.
    It dynamicly changes fold_ss

    Args:
        start(int): starting number.
        end(int): ending number.
        value: value to add.
        current: current frame number
    """
    for num in range(end):
        if num >= start:
            fold_ss[num][0] += value
        if fold_ss[num][1] != 0 and fold_ss[num][1] > current:
            fold_ss[num][1] += value


def score_homogeneity(frame):
    """We are taking value homogenity from database and multiply it 3 times

    Args:
        original_frame: sh-miR object

    Returns:
        Homogeneity score: sh-miR object with modified homogeneity
    """
    return frame.homogeneity * 3


def score_two_same_strands(seq1, original_frame):
    """Points if two strands are indentical

    Args:
        seq1: String with nucleotides.
        original_frame: sh-miR object

    Returns:
        Score for strands (int)
    """
    miRNA_s = original_frame.miRNA_s[:2].upper()
    seq = seq1[:2].upper()
    if seq == miRNA_s:
        return 10
    elif seq[0] == miRNA_s[0]:
        return 4
    return 0


@task
def score_from_sirna(frame, original_frame, folding_file):
    """Function for getting score from siRNA.

    Args:
        frame_tuple: Tuple of frame
        original_frame: sh-miR object
        folding_file: folded structure from mfold

    Returns:
        tuple of score of frame, homogeneity and strands
    """
    structure = score_structure(frame, folding_file, original_frame)
    homogeneity = score_homogeneity(frame)
    same_ends = score_two_same_strands(frame.siRNA1, original_frame)

    return {
        'structure': structure,
        'homogeneity': homogeneity,
        'same_ends': same_ends,
        'all': structure + homogeneity + same_ends
    }


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


def score_from_transcript(
    frame_tuple, original_frame, frame_ss, offtarget, regexp
):
    """
    Function which count score from transcript.

    Args:
        frame_tuple: Tuple of frame
        original_frame: sh-miR object
        frame_ss: file from mfold
        offtarget: Number of transcripts
        regexp: Number of regular expression

    Returns:
        Dict of scores for: frame, offtarget, regexp and all together.
    """
    sframe = score_structure(frame_tuple, frame_ss, original_frame)
    sofftarget = score_offtarget(offtarget)
    sregexp = score_regexp(regexp)
    return {
        'frame': sframe,
        'offtarget': sofftarget,
        'regexp': sregexp,
        'all': sframe + sofftarget + sregexp,
    }
