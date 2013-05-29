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
    return database.get_by_name(request['data'])

@require_data
def get_by_miRNA_s(**request):
    data = str(request['data'])
    if len(data)!=2:
        return {'error': "Data must have 2 characters"}
    return database.get_by_miRNA_s(data)

def backbone_methods(**request):
    methods = {
        'get_by_name': get_by_name,
        'get_all': database.get_all,
        'get_by_miRNA_s': get_by_miRNA_s,
    }
    method = request.pop('method')
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
