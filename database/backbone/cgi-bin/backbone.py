#!/usr/bin/env python3.3

import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import database

print("Content-Type: application/json\n")

response = {'hello_world': True}

print(json.dumps(response))
