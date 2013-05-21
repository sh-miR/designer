import json

def backbone_handler(request):
    dict_response = {'hello_world': True}
    return json.dumps(dict_response)
