"""
.. module:: search
    :synopsis: This module provides searching sequences.
"""

import re


def find_by_patterns(patterns, mRNA):
    """This function search for patterns in mRNA
    :param patterns: List of patterns
    :type patterns: list.
    :param mRNA: mRNA sequnece
    :type mRNA: str.
    :returns: list -- all sequences found by patterns
    """
    sequneces = []
    for pattern in patterns:  # will be changed if not list
        sequneces += re.findall(pattern, mRNA)
    return sequneces
