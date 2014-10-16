"""
.. module:: search
    :synopsis: This module provides searching sequences.
"""

from itertools import chain
from collections import OrderedDict
import re


def findall_overlapping(pattern, string_obj):
    """Function to find by given pattern all overlapping matches in string

    Args:
        pattern(str): Regexp pattern.
        string_obj(str): String in which we search param

    Returns:
        set -- all unique overlapping matches of pattern in string.
    """
    regex = re.compile(pattern)
    results = []
    pos = 0

    while True:
        result = regex.search(string_obj, pos)
        if not result:
            break
        results.append(result.group())
        pos = result.start() + 1
    return set(results)


def find_by_patterns(patterns, mRNA):
    """This function search for patterns in mRNA

    Args:
        patterns: Dict of patterns.
        mRNA(str): mRNA sequnece.

    Returns:
        OrderedDict -- all sequences found by patterns.
    """
    return OrderedDict(sorted([
        (key, chain(*(
            findall_overlapping(pattern, mRNA)
            for pattern in patt_list)
        ))
        for key, patt_list in patterns.items()
    ], reverse=True))


def all_possible_sequences(mRNA, min_len, max_len):
    """This function returns all possible sequneces.

    Args:
        mRNA(str): mRNA sequence.
        min_len(int): Minimum length of mRNA sequence.
        max_len(int): Maximum length of mRNA sequence.

    Returns:
        generator of all possible from min_len to max_len on given mRNA.
    """
    for i in xrange(len(mRNA) - min_len + 1):
        for j in xrange(min_len, max_len + 1):
            sequence = mRNA[i:i+j]
            if len(sequence) == j:
                yield sequence
