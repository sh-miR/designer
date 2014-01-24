"""
Handlers to communicate with database
"""

from shmir_api.database import database
from shmir_api.decorators import jsonify, require_json


@jsonify
def get_all(**kwargs):
    """
    Gets all data from backbone database.
    """
    return database.get_all()


# To immplement in future
#@require_json(require_data=False)
#def get_all_immuno(**kwargs):
#    """
#    Gets all informations from immuno database.
#    """
#    return dumps(immuno.get_all_immuno())


@require_json(required_data_words=1)
def get_by_name(data=None, **kwargs):
    """
    Searching backbone database by name in a case-insensitive way.
    """
    return database.get_by_name(data)


@require_json(required_data_characters=2)
def get_by_miRNA_s(data=None, **kwargs):
    """
    Searching backbone database comparing first two nucleotides of
    endogenous miRNA with two nucleotides of siRNA strand.
    """
    return database.get_by_miRNA_s(data)


get_all.methods = ['POST']
get_by_name.methods = ['POST']
get_by_miRNA_s.methods = ['POST']

# To implement in future
#get_all_immuno.methods = ['POST']
