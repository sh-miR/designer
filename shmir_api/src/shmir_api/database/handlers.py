"""
Handlers to communicate with database
"""

from shmir_api.database import database
from shmir_api.decorators import jsonify, require_json


#backbone
@jsonify
def backbone_get_all(**kwargs):
    """
    Gets all data from backbone database.
    """
    return database.backbone_get_all()


@require_json(required_data_words=1)
def backbone_get_by_name(data=None, **kwargs):
    """
    Searching backbone database by name in a case-insensitive way.
    """
    return database.backbone_get_by_name(data)


@require_json(required_data_characters=2)
def backbone_get_by_miRNA_s(data=None, **kwargs):
    """
    Searching backbone database comparing first two nucleotides of
    endogenous miRNA with two nucleotides of siRNA strand.
    """
    return database.backbone_get_by_miRNA_s(data)


#immuno
@jsonify
def immuno_get_all(**kwargs):
    """
    Gets all informations from immuno database.
    """
    return database.immuno_get_all()


backbone_get_all.methods = ['POST']
backbone_get_by_name.methods = ['POST']
backbone_get_by_miRNA_s.methods = ['POST']
immuno_get_all.methods = ['POST']
