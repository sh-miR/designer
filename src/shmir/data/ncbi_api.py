"""
.. module:: shmir.data.ncbi_api
    :synopsis: Module for connection with ncbi database.
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

    Args:
        email(str): Email to authorization with ncbi.
        transcript(str): Transcript to search.
        database(str): Name of database from ncbi.
        ids(list of str): List of ids to search.
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
    """Function to connect with NCBI database and get transcript by name

    Args:
        transcript(str): name of transcript (from NCBI)
        database: name of database in which we look for (default "nucleotide")
        email(str): email to which NCBI needs to validate

    Returns:
        mRNA(str)

    Raises:
        NoResultError
    """
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
