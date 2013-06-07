#!/usr/bin/env python2.7

import urllib2
import json

url = 'http://127.0.0.1:9001/'
headers = {'content-type': 'application/json'}

class Backbone:
    def __init__(self, name, flanks3_s, flanks3_a, flanks5_s, flanks5_a,\
            loop_s, loop_a, miRNA_s, miRNA_a, miRNA_length, miRNA_min,\
            miRNA_max, structure, homogeneity, miRBase_link):
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
            'structure': self.structure,
            'homogeneity': self.homogeneity,
            'miRBase_link': self.miRBase_link
        }

def qbackbone(method, data=None):
    """
    Acceptable methods(string):
    - get_all
    - get_by_name
    - get_by_miRNA_s
    If you use get_by, you should specify data as a string.
    Returns serialized json data
    """
    json_data = {"method": method}
    if data:
        json_data.update({"data": data})
    req = urllib2.Request(url, json.dumps(json_data), headers)
    return urllib2.urlopen(req).read()
