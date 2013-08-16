"""
Handlers file is an instance to communicate between database and CGI server
"""

import json
import database

from decorators import require_json


@require_json
def get_by_name(request_json):
    """We are searching by name case-insensitive"""
    data = str(request_json['data'])

    if len(data.split()) > 1:
        return {'error': "Data must be one word!"}

    return database.get_by_name(data)


@require_json(require_data=False)
def get_all():
    pass


@require_json
def get_by_miRNA_s(**request):
    """We are searching by only first two nucleotides of endogenous miRNA"""
    data = str(request['data'])

    if len(data) != 2:
        return {'error': "Data must have 2 characters!"}

    return database.get_by_miRNA_s(data)


def backbone_methods(**request):
    methods = {
        'get_by_name': get_by_name,
        'get_all': database.get_all,
        'get_by_mirna_s': get_by_miRNA_s,
    }
    method = request.pop('method').lower()
    if method in methods:
        return methods[method](**request)
    else:
        return {'error': 'Requested method does not exist!'}


def backbone_handler(**request):
    database.connect()
    if 'method' in request:
        response = backbone_methods(**request)
    else:
        response = {'error': 'Method not provided!'}
    database.disconnect()
    return json.dumps(response)
