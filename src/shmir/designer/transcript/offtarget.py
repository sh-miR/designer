"""
.. module:: shmir.designer.transcript.offtarget
    :synopsis: This module connection to Blast and counting offtarget
"""
from operator import itemgetter

from shmir.async import task
from shmir.data.models import (
    db_session,
    Utr,
    HumanmRNA
)


def _count_offtarget(references, with_references=False):
    unique_references = list(set(map(itemgetter(0), references)))
    count = len(unique_references)
    if with_references:
        return {
            'count': count,
            'references': unique_references
        }

    return count


@task
def blast_offtarget(fasta_string, with_references=False):
    references = db_session.query(HumanmRNA.reference).filter(
        HumanmRNA.sequence.like("%{}%".format(fasta_string.upper()))
    )
    return _count_offtarget(references, with_references=with_references)


@task
def offtarget_seed(fasta_string, with_references=False):
    """Function which calculates offtarget using seed sequence on 3'UTR database

    Args:
        fasta_string(str): Fasta sequence.
        with_references(bool):

    Returns:
        Offtarget value(int).

    """
    references = db_session.query(Utr.reference).filter(
        Utr.sequence.like("%{}%".format(fasta_string[1:9].upper()))
    )
    return _count_offtarget(references, with_references=with_references)
