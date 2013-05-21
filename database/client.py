#!/usr/bin/env python3.3

import requests
import json

url = 'http://127.0.0.1:9001/cgi_app.py'
data = {'foo': 'bar'}
headers = {'content-type': 'application/json'}

req = requests.post(url, data=json.dumps(data), headers=headers)
print(req.text)
