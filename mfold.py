import os

import logging

import urllib2
import json
from zipfile import ZipFile


URL = 'http://127.0.0.1:5000/mfold'

HEADERS = {'content-type': 'application/json'}


def mfold(data=None):
    json_data = {'data': data}

    req = urllib2.Request(URL, json.dumps(json_data), HEADERS)
    new_zip = "mfold_files/new.zip"
    try:
        with open(new_zip, "wb") as f:
            f.write(urllib2.urlopen(req).read())
    except urllib2.URLError:
        logging.error('Connection to mfold server refused')
        return {'error': 'Connection to mfold server refused'}
    files = get_list(new_zip)
    os.remove(new_zip)
    return sorted(files)


def get_list(file_path):
    zip_file = ZipFile(file_path)
    zip_list = zip_file.namelist()
    zip_file.extractall(path="mfold_files/")
    zip_list = map(lambda x: "mfold_files/" + x, zip_list)
    return zip_list
