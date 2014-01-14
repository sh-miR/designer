"""
Handlers to communicate with database
"""

from . import database, immuno
from decorators import require_json
from flask.json import dumps

@require_json(require_data=False)
def get_all(**kwargs):
    """
    Gets all data from backbone database.
    """
    return dumps(database.get_all())

@require_json(require_data=False)	
def get_all_immuno(**kwargs):
	"""
	Gets all informations from immuno database.
	"""
	return dumps(immuno.get_all_immuno())


@require_json(required_data_words=1)
def get_by_name(data=None, **kwargs):
    """
    Searching backbone database by name in a case-insensitive way.
    """
    return dumps(database.get_by_name(data))


@require_json(required_data_characters=2)
def get_by_miRNA_s(data=None, **kwargs):
    """
    Searching backbone database comparing first two nucleotides of 
	endogenous miRNA with two nucleotides of siRNA strand. 
    """
    return dumps(database.get_by_miRNA_s(data))


get_all.methods = ['POST']
get_by_name.methods = ['POST']
get_by_miRNA_s.methods = ['POST']
get_all_immuno.methods = ['POST']
