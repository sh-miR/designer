"""
.. module:: shmir.designer.validators
    :synopsis: This module provides input validation.
"""

import re
import math
import errors
import logging
import operator

from shmir.decorators import catch_errors
from utils import reverse_complement
from shmir.data.models import Immuno


def complementarity_level(seq1, seq2):
    """The function gives complementary level of two sequences

    Args:
        seq1(str): first sequence
        seq2(str): second sequence

    Returns:
        Percent of complementary(int)
    """
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
    for molecule1, molecule2 in zip(seq1, seq2):
        if tran[molecule1] == molecule2:
            count += 1
    proc = (count/mini)*100
    return math.floor(proc)


def best_complementarity(seq1, seq2):
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

    Args:
        seq1(str): frist sequence
        seq2(str): second sequence

    Returns:
        tuple (first sequence(str), second sequence(str),
               left offset(int), right offset(int))
    """
    nr_offset = 5
    tab = []
    seq1_len = len(seq1)
    seq2_len = len(seq2)
    end_offset = seq1_len-seq2_len

    if complementarity_level(seq1, seq2) >= 80:
        tab.append((seq1, seq2, 0, end_offset))

    for offset in range(1, nr_offset):
        if complementarity_level(seq1[offset:], seq2) >= 80:
            end_offset = seq1_len-seq2_len-offset
            tab.append((seq1, seq2, offset, end_offset))

        if complementarity_level(seq1, seq2[:-offset]) >= 80:
            end_offset = seq1_len-seq2_len+offset
            tab.append((seq1, seq2, -offset, end_offset))

    if not tab:
        raise errors.ValidationError(errors.orientation_error)

    return max(tab, key=operator.itemgetter(-1))


def replace_mocules(sequence):
    """This function replaces 'u' with 't' molecules
    Rigth end of siRNA is cut if contain 'uu' or 'tt'.

    Args:
        sequence(str)
    Returns
        Tuple of sequence, warning(or None)
    """
    sequence = sequence.upper().replace('U', 'T')
    cut_warn = "cut 'UU' or 'TT'"

    if sequence[-2:] == "TT":
        sequence = sequence[:-2]
        logging.warn(cut_warn)
        return sequence

    return sequence


def validate_sirna(sequence):
    """Function for check sequence from input
    if a single siRNA strand have only actgu letters and is 19-21 nucleotides
    long.

    Args:
        sequence(str): sequence

    Raises:
        ValidationError
    """
    pattern = re.compile(r'^[ACGT]{19,21}$')

    if not pattern.search(sequence):
        if len(sequence) > 21 or len(sequence) < 19:
            raise errors.ValidationError('%s' % errors.len_error)
        raise errors.ValidationError('%s' % errors.patt_error)


@catch_errors(errors.ValidationError)
def parse_input(sirna):
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

    Args:
        sirna: sequence(str) which will be check

    Returns:
        tuple from best_complementarity

    Raises:
        ValidationError
    """
    if " " in sirna:
        sequences = map(replace_mocules, sirna.split(" ", 1))
    else:
        sequences = map(
            replace_mocules,
            [sirna, reverse_complement(sirna)]
        )

    for sequence in sequences:
        validate_sirna(sequence)

    return best_complementarity(*sequences)


def calculate_gc_content(sequence):
    """Function to calculate the GC content.

    Args:
        sequence(str)

    Returns:
        Content of "GC" in sequence
    """
    sequence = sequence.upper()
    g_count = sequence.count('G')
    c_count = sequence.count('C')

    return int((float(g_count + c_count) / len(sequence)) * 100)


def validate_gc_content(sequence, min_percent, max_percent):
    """Function for validate the GC content.

    Args:
        sequence(str),
        min_percent(int): minimal percent of GC content
        max_percent(int): maximal percent of GC content

    Returns:
        bool if sequence has proper GC content
    """
    return min_percent <= calculate_gc_content(sequence) <= max_percent


def validate_immuno(sequence, immuno):
    if immuno == "no_difference":
        return True

    is_immuno = Immuno.check_is_in_sequence(sequence)
    if (is_immuno and immuno == 'yes') or (not is_immuno and immuno == 'no'):
        return True

    return False


def validate_transcript_by_score(score):
    if score['structure'] > 60 and score['all'] > 100:
        return True
    return False
