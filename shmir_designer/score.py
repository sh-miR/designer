"""
.. module:: score
    :synopsis: This module provides scroing frames.
"""

from string import maketrans
from math import ceil
from backbone import Backbone
from ss import parse_ss
from ss import parse_score


def reverse_complement(sequence):
    """Generates reverse complement sequence to given

    input: string
    output: string"""
    sequence = str(sequence)
    return sequence.translate(maketrans("atcgATCG", "tagcTAGC"))[::-1]


def get_frames(seq1, seq2, shift_left, shift_right, all_frames):
    """Take output of check_input function and insert into flanking sequences.
    take from database all miRNA results and check if ends of input is suitable
    for flanking sequences.
    If first value == and miRNA_end_5 second value == miRNA_end_3 then simply
    concatenate
    sequences flanks5_s + first_sequence + loop_s + second_sequence + flanks3_s.
    If any end is different function has to modify end of the insert:
    Right end:
    if miRNA_end_5 < first_end
    add to right site of second sequence additional nucleotides
    (as many as |miRNA_end_5 - first_end|) like
    (dots are nucleotides to add, big letter are flanking sequences, small are input):

    AAAGGGGCTTTTagtcttaga
    TTTCCCCGAA....agaatct

    if miRNA_end_5 > first_end
    cut nucleotides from rigth site of flanks3_s and/or from right site of
    second sequence

    before cut:
    AAAGGGGCTTTTagtcttaga
    TTTCCCCGAAAATTcctcagaatct (-2, +2)

    After
    AAAGGGGCTTTTagtcttaga
    TTTCCCCGAAAAtcagaatct

    Returns list of tuples (frame, sequence_1 sequence_2)

    Nucleotides are always added to the right side of sequences.
    We cut off nucleotides only from flanking sequences or loop.

    input: string, string, int, int, pri-miRNA objects
    output: List of list of Backbone object, 1st strand 2nd strand   """
    frames = []
    for elem in all_frames:
        frame = Backbone(**elem)
        if shift_left == frame.miRNA_end_5 and shift_right == frame.miRNA_end_5:
            frames.append([frame, seq1, seq2])
        else:
            _seq1 = seq1[:]
            _seq2 = seq2[:]
            #miRNA 5 end (left)
            if frame.miRNA_end_5 < shift_left:
                if frame.miRNA_end_5 < 0 and shift_left < 0:
                    _seq2 += reverse_complement(
                        frame.flanks5_s[frame.miRNA_end_5:shift_left])
                elif frame.miRNA_end_5 < 0 and shift_left > 0:
                    frame.flanks5_s = frame.flanks5_s[:frame.miRNA_end_5]
                    _seq2 += reverse_complement(_seq1[:shift_left])
                elif shift_left == 0:
                    _seq2 += reverse_complement(
                        frame.flanks5_s[:frame.miRNA_end_5])
                elif frame.miRNA_end_5 == 0:
                    _seq2 += reverse_complement(_seq1[:frame.miRNA_end_5])
                else:
                    _seq2 += reverse_complement(
                        _seq1[frame.miRNA_end_5:shift_left])
            elif frame.miRNA_end_5 > shift_left:
                if frame.miRNA_end_5 > 0 and shift_left < 0:
                    frame.flanks5_s += reverse_complement(
                        _seq2[frame.miRNA_end_5:])
                    frame.flanks3_s = frame.flanks3_s[frame.miRNA_end_5:]
                elif frame.miRNA_end_5 > 0 and shift_left > 0:
                    frame.flanks5_s += reverse_complement(
                        frame.flanks3_s[shift_left:frame.miRNA_end_5])
                elif shift_left == 0:
                    frame.flanks5_s += reverse_complement(
                        frame.flanks3_s[:frame.miRNA_end_5])
                elif frame.miRNA_end_5 == 0:
                    frame.flanks5_s += reverse_complement(_seq2[shift_left:])
                else:
                    frame.flanks5_s += reverse_complement(
                        _seq2[shift_left:frame.miRNA_end_5])

            #miRNA 3 end (right)
            if frame.miRNA_end_3 < shift_right:
                if frame.miRNA_end_3 < 0 and shift_right > 0:
                    frame.loop_s = frame.loop_s[-frame.miRNA_end_3:]
                    frame.loop_s += reverse_complement(
                        _seq1[-shift_right:])
                elif frame.miRNA_end_3 > 0 and shift_right > 0:
                    frame.loop_s += reverse_complement(
                        _seq1[-shift_right:-frame.miRNA_end_3])
                elif frame.miRNA_end_3 == 0:
                    frame.loop_s += reverse_complement(_seq1[-shift_right:])
                elif shift_right == 0:
                    frame.loop_s += reverse_complement(
                        frame.loop_s[:-frame.miRNA_end_3])
                else:
                    frame.loop_s += reverse_complement(
                        frame.loop_s[-shift_right:-frame.miRNA_end_3])
            elif frame.miRNA_end_3 > shift_right:
                if frame.miRNA_end_3 > 0 and shift_right < 0:
                    _seq1 += reverse_complement(
                        _seq2[:-shift_right])
                    frame.loop_s = frame.loop_s[:-frame.miRNA_end_3]
                elif frame.miRNA_end_3 > 0 and shift_right > 0:
                    _seq1 += reverse_complement(
                        frame.loop_s[-frame.miRNA_end_3:-shift_right])
                elif shift_right == 0:
                    _seq1 += reverse_complement(
                        frame.loop_s[:frame.miRNA_end_3])
                elif frame.miRNA_end_3 == 0:
                    _seq1 += reverse_complement(_seq2[:-shift_right])
                else:
                    _seq1 += reverse_complement(
                        _seq2[-frame.miRNA_end_3:-shift_right])

            frames.append([frame, _seq1, _seq2])
    return frames


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
    for shmir in structure_ss:
        for template in orginal_score:
            if shmir == template[0]:
                score += template[1]
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
    miRNA_s = original_frame.miRNA_s[:2].lower()
    seq = seq1[:2].lower()
    if seq == miRNA_s:
        return 10
    elif seq[0] == miRNA_s[0]:
        return 4
    else:
        return 0
