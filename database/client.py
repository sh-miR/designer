#!/usr/bin/env python2.7

import urllib2
import json

url = 'http://127.0.0.1:9001/'
data = {'foo': 'bar'}
headers = {'content-type': 'application/json'}

req = urllib2.Request(url, json.dumps(data), headers)

resp = urllib2.urlopen(req)
print(resp.read())
resp.close()
