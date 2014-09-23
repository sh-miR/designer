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

    #differences
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
        left, right = frame_ss[num]
        if num >= start:
            left += value
        if right != 0 and right > current:
            right += value


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
    else:
        return 0
