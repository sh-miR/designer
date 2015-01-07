"""
.. module:: shmir.designer.sirnascore
    :synopsis: This module provides scoring sh-miRs created from siRNA.
"""

from shmir.designer.mfold.score import score_structure
from shmir.async import task


def score_homogeneity(frame):
    """We are taking value homogenity from database and multiply it 3 times

    Args:
        original_frame: sh-miR object

    Returns:
        Homogeneity score: sh-miR object with modified homogeneity
    """
    return frame.homogeneity * 3


def score_two_same_strands(seq1, original_frame):
    """Points if two strands are indentical

    Args:
        seq1: String with nucleotides.
        original_frame: sh-miR object

    Returns:
        Score for strands (int)
    """
    miRNA_s = original_frame.miRNA_s[:2].upper()
    seq = seq1[:2].upper()
    if seq == miRNA_s:
        return 10
    elif seq[0] == miRNA_s[0]:
        return 4
    return 0


@task
def score_from_sirna(frame, original_frame, folding_file):
    """Function for getting score from siRNA.

    Args:
        frame_tuple: Tuple of frame
        original_frame: sh-miR object
        folding_file: folded structure from mfold

    Returns:
        tuple of score of frame, homogeneity and strands
    """
    structure = score_structure(frame, folding_file, original_frame)
    homogeneity = score_homogeneity(frame)
    same_ends = score_two_same_strands(frame.siRNA1, original_frame)

    return {
        'structure': structure,
        'homogeneity': homogeneity,
        'same_ends': same_ends,
        'all': structure + homogeneity + same_ends
    }
