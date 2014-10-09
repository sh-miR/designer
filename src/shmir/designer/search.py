"""
.. module:: search
    :synopsis: This module provides searching sequences.
"""

from itertools import chain
from collections import OrderedDict
import re


def findall_overlapping(pattern, string):
    """
    :param pattern: Pattern string.
    :type pattern: str.
    :param string: String in which we search.param
    :type string: str.
    :returns: set -- all unique overlapping matches of pattern in string.
    """
    regex = re.compile(pattern)
    results = []
    pos = 0

    while True:
        result = regex.search(string, pos)
        if not result:
            break
        results.append(result.group())
        pos = result.start() + 1
    return set(results)


def find_by_patterns(patterns, mRNA):
    """This function search for patterns in mRNA
    :param patterns: Dict of patterns.
    :type patterns: dict.
    :param mRNA: mRNA sequnece.
    :type mRNA: str.
    :returns: OrderedDict -- all sequences found by patterns.
    """
    return OrderedDict(sorted([
        (key, chain(*(
            findall_overlapping(pattern, mRNA)
            for pattern in patt_list)
        ))
        for key, patt_list in patterns.items()
    ], reverse=True))


def all_possible_sequences(mRNA, min_len, max_len):
    """
    This function returns all possible sequneces.
    :param mRNA: mRNA sequence.
    :type mRNA: str.
    :param min_len: Minimum length of mRNA sequence.
    :type min_len: int.
    :param max_len: Maximum length of mRNA sequence.
    :type max_len: int.
    :returns: generator.
    """
    for i in xrange(len(mRNA) - min_len + 1):
        for j in xrange(min_len, max_len + 1):
            sequence = mRNA[i:i+j]
            if len(sequence) == j:
                yield sequence
