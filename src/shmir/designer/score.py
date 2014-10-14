"""
.. module:: score
    :synopsis: This module provides scroing frames.
"""

from math import ceil
from .ss import parse_ss
from .ss import parse_score


def score_frame(frame, frame_ss_file, orginal_frame):
    """Frame is a tuple of object Backbone and two sequences
    frame_ss_file is file from mfold
    orignal_frame is object Backbone from database (not changed)

    input: sh-miR object, ss_file, ss_file
    output: int"""

    structure, seq1, seq2 = frame
    structure_ss = parse_ss(frame_ss_file)
    max_score, orginal_score = parse_score(u'.' + orginal_frame.structure)

    # differences
    flanks5 = len(orginal_frame.flanks5_s) - len(structure.flanks5_s)
    insertion1 = len(orginal_frame.miRNA_s) - len(seq1)
    loop = len(orginal_frame.loop_s) - len(structure.loop_s)
    insertion2 = len(orginal_frame.miRNA_a) - len(seq2)
    flanks3 = len(orginal_frame.flanks3_s) - len(structure.flanks3_s)

    position = len(structure.flanks5_s)  # position in sequence (list)
    structure_len = len(structure.template(seq1, seq2))
    current = position + flanks5  # current position (after changes)

    if flanks5 < 0:
        add_shifts(0, structure_len, structure_ss, flanks5, 0)
    else:
        add_shifts(position, structure_len,
                   structure_ss, flanks5, current)
    for diff, nucleotides in [(insertion1, seq1), (loop, structure.loop_s),
                              (insertion2, seq2), (flanks3, '')]:
        position += len(nucleotides)
        current = position + diff
        add_shifts(position, structure_len, structure_ss, diff, current)
    score = 0
    for created in structure_ss:
        for orginal, points in orginal_score:
            if created == orginal:
                score += points
    return int(ceil(score/max_score * 100))


def add_shifts(start, end, frame_ss, value, current):
    """The numbers assigned to the nucleotides have to be verified,
    because flanking sequences can be shortened or extended during insertion.
    Moreover, the length of the siRNA insert can differ from the natural one.

    input: start, end, frame_ss, value, current.
    The function has no output"""
    for num in range(end):
        if num >= start:
            frame_ss[num][0] += value
        if frame_ss[num][1] != 0 and frame_ss[num][1] > current:
            frame_ss[num][1] += value


def score_homogeneity(original_frame):
    """We are taking value homogenity from database and multiply it 3 times

    input: sh-miR object
    output: sh-miR object with modified homogeneity"""
    return original_frame.homogeneity * 3


def score_two_same_strands(seq1, original_frame):
    """Input: string, pri-miRNA object.
    The function has no output."""
    miRNA_s = original_frame.miRNA_s[:2].upper()
    seq = seq1[:2].upper()
    if seq == miRNA_s:
        return 10
    elif seq[0] == miRNA_s[0]:
        return 4
    return 0


def score_from_sirna(frame_tuple, original_frame, frame_ss, sequence):
    """
    Function for getting score from siRNA.
    input: frame_tuple, original_frame, frame_ss, sequence
    output: tuple.
    """
    return (
        score_frame(frame_tuple, frame_ss, original_frame) +
        score_homogeneity(original_frame) +
        score_two_same_strands(sequence, original_frame)
    )


def score_offtarget(number):
    """
    Function counts score.
    input: number
    output: int.
    """
    score = 40 - number * 2
    if score >= 0:
        return score
    return 0


def score_regexp(number):
    """
    input: int.
    output: int.
    """
    return number * 5


def score_from_transcript(
    frame_tuple, original_frame, frame_ss, offtarget, regexp
):
    """
    Function which count score from transcript.
    input: frame_tuple, original_frame, frame_ss, offtarget, regexp
    output: dict.
    """
    sframe = score_frame(frame_tuple, frame_ss, original_frame)
    sofftarget = score_offtarget(offtarget)
    sregexp = score_regexp(regexp)
    return {
        'frame': sframe,
        'offtarget': sofftarget,
        'regexp': sregexp,
        'all': sframe + sofftarget + sregexp,
    }
