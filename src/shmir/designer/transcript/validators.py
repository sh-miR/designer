"""
.. module:: shmir.designer.transcript.validators
    :synopsis: This module provides validation for sequences created from transcript
"""

from shmir.data.models import Immuno


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
    return (is_immuno and immuno == 'yes') or (not is_immuno and immuno == 'no')


def validate_transcript_by_score(score):
    return score['structure'] > 60 and score['all'] > 100
