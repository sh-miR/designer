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
