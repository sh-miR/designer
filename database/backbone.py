#!/usr/bin/env python3.3

import json

def backbone(environ, start_response):
    dict_response = {'hello_world': True}
    return json.dumps(dict_response)
