"""
Module for connection with ncbi database.
"""

import json

from Bio import Entrez


def make_authorize_for_ncbi(email):
    """
    Function which makes authorization in ncbi database with given email.

    :param email: Email to authorization with ncbi.
    :type email: str.
    """
    Entrez.email = email


def get_ids_of_searched_term(email, transcript, database):
    """
    Function for retrieve list of ids for searched transcript
    (transcript should be URL encoded) from given ncbi database.

    :param email: Email to authorization with ncbi.
    :type email: str.
    :param transcript: Transcript to search.
    :type transcript: str.
    :param database: Name of database from ncbi.
    :type database: str.

    List of avaible ncbi database:
        ['pubmed', 'protein', 'nucleotide', 'nuccore', 'nucgss', 'nucest',
         'structure', 'genome', 'books', 'cancerchromosomes', 'cdd', 'gap',
         'domains', 'gene', 'genomeprj', 'gensat', 'geo', 'gds', 'homologene',
         'journals', 'mesh', 'ncbisearch', 'nlmcatalog', 'omia', 'omim', 'pmc',
         'popset', 'probe', 'proteinclusters', 'pcassay', 'pccompound',
         'pcsubstance', 'snp', 'taxonomy', 'toolkit', 'unigene', 'unists']
    """
    make_authorize_for_ncbi(email)

    handle = Entrez.esearch(db=database, term=transcript, retmode='json')

    json_results = handle.read(handle)
    results = json.loads(json_results)

    return results['esearchresult']['idlist']


def get_data(email, database, ids):
    """
    Function for return data from given ncbi database by given list of ids.

    :param email: Email to authorization with ncbi.
    :type email: str.
    :param database: Name of database from ncbi.
    :type database: str.
    :param ids: List of ids to search.
    :type ids: list/str.
    """
    make_authorize_for_ncbi(email)

    fasta_sequnce = Entrez.efetch(
        db=database,
        id=ids,
        rettype='fasta',
        retmode="text"
    ).read()

    return fasta_sequnce
