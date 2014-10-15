"""
.. module:: shmir.designer.utils
    :synopsis: This module provides side functions.
"""

from string import maketrans
from itertools import (
    chain,
    izip_longest,
)
from operator import is_not
from functools import partial


def reverse_complement(sequence):
    """Generates reverse complement sequence to given

    Args:
        sequence(str).

    Returns:
        revese complement sequence(str) to given.
    """
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
    (dots are nucleotides to add, big letter are flanking sequences, small are
    input):

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

    Nucleotides are always added to the right side of sequences.
    We cut off nucleotides only from flanking sequences or loop.

    Args:
        seq1(str) first sequence.
        seq2(str) second sequence.
        shift_left(int) - shift on sequence from left side.
        shift_right(int) - shift on sequence from right side.
        all_frames(pri-miRNA objects) frames from which we create sh-miRs.

    Returns:
        list of tuples (changed frame, first sequence, second sequence).
    """
    frames = []
    for frame in all_frames:
        _seq1 = seq1[:]
        _seq2 = seq2[:]
        # switch active strand
        if frame.active_strand == 3:
            _seq1, _seq2 = _seq2, _seq1

        if shift_left == frame.miRNA_end_5 and shift_right == frame.miRNA_end_5:
            frames.append([frame, _seq1, _seq2])
        else:
            # miRNA 5 end (left)
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

            # miRNA 3 end (right)
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


def unpack_dict_to_list(dict_object):
    """
    Function to unpack dict to list.
    It "dequeues" {'a': ['b', 'c'], 'd': ['e', 'f'], ...} into
    ['b', 'e', 'c', 'f'] (for one from each dict)

    Args:
        dict_object: Dict object to unpack.

    Returns:
        List of unpacked values from dict.
    """
    to_zip = [[(key, elem) for elem in dict_object[key]] for key in dict_object]
    return (elem for inner_list in izip_longest(*to_zip)
            for elem in inner_list if elem is not None)


def remove_none(list_object):
    """
    Function which removes None objects from list.

    Args:
        list_object: List.

    Returns:
        List of object which are not None.
    """
    return filter(partial(is_not, None), list_object)


def generator_is_empty(generator):
    """
    Function which check if a generator is empty.
    Args:
        generator: Generator object.

    Returns:
        List with 2 elements: (Bool, Generator) or (Bool, None)
    """
    try:
        first = next(generator)
    except StopIteration:
        return True, None
    return False, chain([first], generator)
