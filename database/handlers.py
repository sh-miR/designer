from functools import wraps
import json
import database

def require_data(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'data' in kwargs:
            return f(*args, **kwargs)
        return {'error': 'Data not provided!'}
    return decorated

@require_data
def get_by_name(**request):
    return database.get_by_name(request['data']).serialize()

def backbone_methods(**request):
    if request['method'] == 'get_by_name':
        return get_by_name(**request)
    if request['method'] == 'get_all':
        return [backbone.serialize() for backbone in database.get_all()]
    return {'error': 'Requested method does not exist!'}

def backbone_handler(**request):
    if 'method' in request:
        response = backbone_methods(**request)
    else:
        response = {'error': 'Method not provided!'}
    return json.dumps(response)
