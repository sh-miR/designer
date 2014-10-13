"""
.. module:: validators
    :synopsis: This module provides input validation.
"""

import re
import math
import errors
import logging

from urllib2 import HTTPError
from shmir.data.models import Immuno
from shmir.designer.offtarget import blast_offtarget


def check_complementary_single(seq1, seq2):
    """The function checks complementary of two sequences

    input: string, string
    output: int"""
    seq1, seq2 = seq1.upper(), seq2.upper()
    tran = {
        "A": "T",
        "T": "A",
        "U": "A",
        "C": "G",
        "G": "C"
    }
    seq2 = seq2[::-1]
    mini = float(min(len(seq1), len(seq2)))
    count = 0
    for mol1, mol2 in zip(seq1, seq2):
        if tran[mol1] == mol2:
            count += 1
    proc = (count/mini)*100
    return math.floor(proc)


def check_complementary(seq1, seq2):
    """Test for complementary, if both strands are in 5'-3' orientation
    class perform only when there are two strands given; should take as input
    both strand,
    input:
    * 5'acggcttGGaactuctggtac3'
    * 5'gtaccagaagttccaagccgt3'
    reverse second:
    * 3'tgccgaaccttgaagaccatg5'
    translate second strand in a way (a->t, t->a, u->a, c->g, g->c),
    * 5'acggcttGGaactuctggtac3'
    check if the strands are the same,
    starting with first nucleotide or -2,-1,
    +1,+2 (from the beggining or the end) with minimum 80% similarity

    3) 5'acggcttGGaactuctggtac3'
         |||||||||||||||||||||
       3'tgccgaaccttgaagaccatg5'
       5'acggcttGGaactuctggtac3'

    output: 'first sequence' (19-21nt), 'second sequence' (19-21nt), left_end
    {-4,-3,-2,-1,0,1,2,3,4}, rigth_end{-4,-3,-2,-1,0,1,2,3,4}

    input: string, string

    output: tuple (string, string, int, int)"""
    nr_offset = 5
    tab = []
    end_offset = len(seq1)-len(seq2)
    if check_complementary_single(seq1, seq2) >= 80:
        tab.append((seq1, seq2, 0, end_offset))

    for offset in range(1, nr_offset):
        if check_complementary_single(seq1[offset:], seq2) >= 80:
            end_offset = len(seq1)-len(seq2)-offset
            tab.append((seq1, seq2, offset, end_offset))
        if check_complementary_single(seq1, seq2[:-offset]) >= 80:
            end_offset = len(seq1)-len(seq2)+offset
            tab.append((seq1, seq2, -offset, end_offset))
    if not tab:
        raise errors.ValidationError(errors.error)
    return tab[0]


def check_input_single(seq):
    """Function for check sequence from input
    if a single siRNA strand have only actgu letters and is 19-21 nucleotides
    long.
    Also rigth end of siRNA is cut if contain 'uu' or 'tt'.
    Input: string;
    The function has no output"""
    seq = seq.upper().replace('U', 'T')
    pattern = re.compile(r'^[ACGT]{19,21}$')
    cut_warn = "cut 'UU' or 'TT'"

    if not pattern.search(seq):
        if len(seq) > 21 or len(seq) < 19:
            raise errors.ValidationError('%s' % errors.len_error)
        raise errors.ValidationError('%s' % errors.patt_error)
    elif seq[-2:] == "TT" and pattern.search(seq):
        seq = seq[:-2]
        logging.warn(cut_warn)
        return [seq, cut_warn, True]
    elif pattern.search(seq):
        return [seq, None, True]


def check_input(seq_to_be_check):
    """Function for checking many sequences and throw error if wrong input
    input limitations: possible letters: {ACTGUactgu}, change all 'u' to 't',
    length 19-21, one strand or two strands splitted by space,
    if two strands check if they are in correct 5'-3' orientation, allow |_20%_|
    mismatches,
    if the sequence is correct input returns 'first sequence' (19-21nt), 'second
    sequence' (19-21nt), left_end{-4,-3,-2,-1,0,1,2,3,4},
    rigth_end{-4,-3,-2,-1,0,1,2,3,4}
    messages:
    * "correct sequence"
    * "changed 'u' to 't'"
    * "cut 'uu' or 'tt' ends"
    errors:
    * "too short"
    * "insert your siRNA sequence"
    * "too long"
    * "insert only one siRNA sequence or both strands of one siRNA at a time;
    check if both stands are in 5'-3' orientation"
    * "sequence can contain only {actgu} letters

    input: string
    output: output of check_complementary"""
    sequence = seq_to_be_check.split(" ")
    len_seq = len(sequence)
    if len_seq == 1:
        return (check_input_single(sequence[0])[0], '', 0, 0)
    elif len_seq == 2:
        ch_seq1 = check_input_single(sequence[0])
        ch_seq2 = check_input_single(sequence[1])
        if ch_seq1[2] and ch_seq2[2]:
            return check_complementary(ch_seq1[0], ch_seq2[0])
    else:
        raise errors.ValidationError('{}'.format(errors.error))


def calculate_gc_content(sequence):
    """
    Function to calculate the GC content.
    input: str.
    output: int
    """
    sequence = sequence.upper()
    g_count = sequence.count('G')
    c_count = sequence.count('C')

    return int((float(g_count + c_count) / len(sequence)) * 100)


def validate_gc_content(sequence, min_percent, max_percent):
    """
    Function for validate the GC content.
    input: sequence, min_percent, max_percent
    output: bool.
    """
    return min_percent <= calculate_gc_content(sequence) <= max_percent


def validate_sequence(sequence, max_offtarget, min_gc, max_gc, stimulatory):
    """
    Function to validate sequence.
    input: sequence, max_offtarget, min_gc, max_gc, stimulatory
    output: tuple.
    """
    gc = validate_gc_content(sequence, min_gc, max_gc)
    is_immuno = Immuno.check_is_in_sequence(sequence)

    if gc and (
            stimulatory == 'no_difference' or
            (is_immuno and stimulatory == 'yes') or
            (not is_immuno and stimulatory == 'no')
    ):
        # when debuging uncomment return
        # return True, 0
        try:
            actual_offtarget = blast_offtarget(sequence)
        except HTTPError:
            return False, None
        offtarget = actual_offtarget <= max_offtarget
        if offtarget:
            return True, actual_offtarget

    return False, None
