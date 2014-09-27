"""
Module for connection with ncbi database.
"""

import json
import re

from Bio import Entrez
from shmir.designer import errors
from shmir import settings


def get_data(
    transcript, database=settings.NUCLEOTIDE_DB, email=settings.EMAIL
):
    """
    Function responsible to get data from given ncbi database.

    :param email: Email to authorization with ncbi.
    :type email: str.
    :param transcript: Transcript to search.
    :type transcript: str.
    :param database: Name of database from ncbi.
    :type database: str.
    :param ids: List of ids to search.
    :type ids: list/str.
    """
    Entrez.email = email
    handle = Entrez.esearch(
        db=database,
        term=transcript,
        retmode='json'
    )

    json_results = handle.read(handle)
    ids = json.loads(json_results)['esearchresult']['idlist']

    return Entrez.efetch(
        db=database,
        id=ids,
        rettype='fasta',
        retmode='text'
    ).read()


def get_mRNA(transcript, database=settings.NUCLEOTIDE_DB, email=settings.EMAIL):
    pattern = re.compile(r'^NM_[0-9]+[.]{1}[0-9]+$')
    mrna = 'mRNA'

    if not re.match(pattern, transcript):
        raise errors.IncorrectDataError('Invalid transcript format.')

    data = get_data(transcript)

    limit = data.find(mrna)

    if limit != -1:
        return data[limit + len(mrna):].replace('\n', '')
    else:
        raise errors.NoResultError(
            '{} not found in database.'.format(transcript)
        )
