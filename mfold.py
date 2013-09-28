import urllib2
import json

URL = 'http://127.0.0.1:5000/mfold'

HEADERS = {'content-type': 'application/json'}


def mfold(data=None):
    json_data = {'data': data}

    #import pdb
    #pdb.set_trace()

    req = urllib2.Request(URL, json.dumps(json_data), HEADERS)

    try:
        return json.loads(urllib2.urlopen(req).read())
    except urllib2.URLError:
        return {'error': 'Connection to database refused'}
