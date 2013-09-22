"""
Handlers file is an instance to communicate with database
"""

from flask import jsonify

import database
from decorators import require_json


@require_json(require_data=False)
def get_all():
    return jsonify(database.get_all())


@require_json
def get_by_name(request_json):
    """
    We are searching by name case-insensitive

    """

    data = str(request_json['data'])

    if len(data.split()) > 1:
        return jsonify(error="Data must be one word!")

    return jsonify(database.get_by_name(data))


@require_json
def get_by_miRNA_s(**request):
    """
    We are searching by only first two nucleotides of endogenous miRNA

    """

    data = str(request['data'])

    if len(data) != 2:
        return jsonify(error="Data must have 2 characters!")

    return jsonify(database.get_by_miRNA_s(data))
