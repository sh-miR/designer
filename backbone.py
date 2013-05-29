#!/usr/bin/env python2.7

import urllib2
import json

url = 'http://127.0.0.1:9001/'
headers = {'content-type': 'application/json'}

def qbackbone(method, data=None):
    """
    Acceptable methods(string):
    - get_all
    - get_by_name
    - get_by_miRNA_s
    If you use get_by, you should specify data as a string.
    """
    json_data = {"method": method}
    if data:
        json_data.update({"data": data})
    req = urllib2.Request(url, json.dumps(json_data), headers)
    return urllib2.urlopen(req).read()
