"""
.. module:: shmir.designer.transcript.utils
    :synopsis: This module provides side functions.
"""

from itertools import (
    chain,
    izip_longest,
    ifilter,
)
from collections import defaultdict


def unpack_dict_to_list(dict_object):
    """
    Function to unpack dict to list.
    It "dequeues" {'a': ['b', 'c'], 'd': ['e', 'f'], ...} into
    [('a', 'b'), ('d', 'e'), ('a', 'c'), ('d', 'f')] (for one from each dict)

    Args:
        dict_object: Dict object to unpack.

    Returns:
        List of unpacked values from dict.
    """
    # create tuples (key, value)
    to_zip = [[(key, elem) for elem in dict_object[key]] for key in dict_object]
    return ifilter(None, chain(*izip_longest(*to_zip)))


def create_path_string(*args):
    return "_".join(map(str, args))


def merge_results(validated):
    best_sequences = defaultdict(list)
    for valid_group in validated:
        for name, sequences in valid_group.iteritems():
            best_sequences[name] += sequences
    return best_sequences
