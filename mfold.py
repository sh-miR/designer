import urllib2
import json
from zipfile import ZipFile

URL = 'http://127.0.0.1:5000/mfold'

HEADERS = {'content-type': 'application/json'}


def mfold(data=None):
    json_data = {'data': data}

    req = urllib2.Request(URL, json.dumps(json_data), HEADERS)

    with open("dat.zip", "wb") as f:
        f.write(urllib2.urlopen(req).read())


    # try:
    #     return json.loads(urllib2.urlopen(req).read())
    # except urllib2.URLError:
    #     return {'error': 'Connection to database refused'}
