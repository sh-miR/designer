#!/usr/bin/env python2.7

import requests
import json

HOST = 'http://127.0.0.1:5000/'
URL_ALL = HOST + 'database/get_all'
URL_BY_NAME = HOST + 'database/get_by_name'
URL_BY_MIRNA_S = HOST + 'database/get_by_mirna_s'

HEADERS = {'content-type': 'application/json'}


class Backbone:
    def __init__(self, name, flanks3_s, flanks3_a, flanks5_s, flanks5_a,
                 loop_s, loop_a, miRNA_s, miRNA_a, miRNA_length, miRNA_min,
                 miRNA_max, miRNA_end_5, miRNA_end_3, structure, homogeneity,
                 miRBase_link):
        self.name = name
        self.flanks3_s = flanks3_s
        self.flanks3_a = flanks3_a
        self.flanks5_s = flanks5_s
        self.flanks5_a = flanks5_a
        self.loop_s = loop_s
        self.loop_a = loop_a
        self.miRNA_s = miRNA_s
        self.miRNA_a = miRNA_a
        self.miRNA_length = miRNA_length
        self.miRNA_min = miRNA_min
        self.miRNA_max = miRNA_max
        self.miRNA_end_5 = miRNA_end_5
        self.miRNA_end_3 = miRNA_end_3
        self.structure = structure
        self.homogeneity = homogeneity
        self.miRBase_link = miRBase_link

    def serialize(self):
        return {
            'name': self.name,
            'flanks3_s': self.flanks3_s,
            'flanks3_a': self.flanks3_a,
            'flanks5_s': self.flanks5_s,
            'flanks5_a': self.flanks5_a,
            'loop_s': self.loop_s,
            'loop_a': self.loop_a,
            'miRNA_s': self.miRNA_s,
            'miRNA_a': self.miRNA_a,
            'miRNA_length': self.miRNA_length,
            'miRNA_min': self.miRNA_min,
            'miRNA_max': self.miRNA_max,
            'miRNA_end_5': self.miRNA_end_5,
            'miRNA_end_3': self.miRNA_end_3,
            'structure': self.structure,
            'homogeneity': self.homogeneity,
            'miRBase_link': self.miRBase_link
        }

    def template(self, siRNAstrand_1, siRNAstrand_2):
        """Returns the template of DNA"""
        return self.flanks5_s + siRNAstrand_1 + self.loop_s +\
            siRNAstrand_2 + self.flanks3_s


def qbackbone(data=None, url=None):
    """
    Acceptable methods(string):
    - get_all
    - get_by_name
    - get_by_miRNA_s
    If you use get_by, you should specify data as a string.
    Returns serialized json data
    """

    json_data = {}
    if data:
        json_data.update({"data": data})
    req = requests.post(url, json.dumps(json_data), headers=HEADERS)
    try:
        return json.loads(req.content)
    except requests.ConnectionError:
        return {'error': 'Connection to database refused.'}


def get_all(data=None):
    return qbackbone(data=data, url=URL_ALL)


def get_by_name(data=None):
    return qbackbone(data=data, url=URL_BY_NAME)


def get_by_mirna_s(data=None):
    return qbackbone(data=data, url=URL_BY_MIRNA_S)
