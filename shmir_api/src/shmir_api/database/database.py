"""
Module for communication with database
"""

from __future__ import print_function, unicode_literals

import psycopg2
from flask import g

from shmir_api.settings import DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT


def get_db():
    """
    Global connector variable
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = psycopg2.connect(database=DB_NAME, user=DB_USER,
                              password=DB_PASS, host=DB_HOST, port=DB_PORT)
    return db


def disconnect():
    """
    Global disconnector
    """
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def execute_with_one_response(query, var=None):
    """
    Executes query and returns only first response
    """
    with get_db().cursor() as cur:
        cur.execute(query, var)
        data = cur.fetchone()
    return data


def execute_with_response(query, var=None):
    """
    Executes query and returns all responses
    """
    with get_db().cursor() as cur:
        cur.execute(query, var)
        data = cur.fetchall()
        cur.close()
    return data


def get_multirow_by_query(query, var=None):
    """
    Returns serialized data from backbone table
    """
    data = execute_with_response(query, var)
    backbones = []
    for row in data:
        backbones.append(serialize(*row))
    return backbones


def get_multirow_by_query_immuno(query, var=None):
    """
    Returns serialized data from immuno table
    """
    data = execute_with_response(query, var)
    immuno_seq = []
    for row in data:
        immuno_seq.append(serialize_immuno(*row))
    return immuno_seq


def add(name, flanks3_s, flanks3_a, flanks5_s, flanks5_a, loop_s, loop_a,
        miRNA_s, mirRNA_a, miRNA_length, miRNA_min, miRNA_max, miRNA_end_5,
        miRNA_end_3, structure, homogeneity, miRBase_link, active_strand):
    """
    Function which adds another miRNA backbone record to database without
    closing server
    """

    query = ("INSERT INTO backbone VALUES(DEFAULT, %s, %s, %s, %s, %s, %s, %s,"
             " %s, %s, %d, %d, %d, %s, %d, %s, %d);")

    var = (name, flanks3_s, flanks3_a, flanks5_s, flanks5_a, loop_s, loop_a,
           miRNA_s, mirRNA_a, miRNA_length, miRNA_min, miRNA_max, miRNA_end_5,
           miRNA_end_3, structure, homogeneity, miRBase_link, active_strand)

    with get_db().cursor() as cur:
        cur.execute(query, var)


def get_by_name(name):
    """
    Function which gets one serialized Backbone by name
    """
    query = ("SELECT name, flanks3_s, flanks3_a, flanks5_s, flanks5_a, loop_s,"
             " loop_a, miRNA_s, miRNA_a, miRNA_length, miRNA_min, miRNA_max, "
             "miRNA_end_5, miRNA_end_3, structure, homogeneity, miRBase_link, "
             "active_strand FROM backbone WHERE LOWER(name) = LOWER(%s);")

    data = execute_with_one_response(query, (name,))

    return serialize(*data) if data else {}


def get_all():
    """
    Function which gets all serialized Backbones in database
    """
    query = ("SELECT name, flanks3_s, flanks3_a, flanks5_s, flanks5_a, loop_s,"
             " loop_a, miRNA_s, miRNA_a, miRNA_length, miRNA_min, miRNA_max, "
             "miRNA_end_5, miRNA_end_3, structure, homogeneity, miRBase_link, "
             "active_strand FROM backbone;")

    return get_multirow_by_query(query)


def get_all_immuno():
    """
    Function which gets all serialized immuno sequences in database
    """
    query = ("SELECT sequence, receptor, link"
             "FROM immuno;")

    return get_multirow_by_query_immuno(query)


def get_by_miRNA_s(letters):
    """
    Function which gets serialized Backbones having first two letters of
    miRNA_s same as letters given (first two nucleotides of siRNA strand)
    """
    query = ("SELECT name, flanks3_s, flanks3_a, flanks5_s, flanks5_a, loop_s,"
             " loop_a, miRNA_s, miRNA_a, miRNA_length, miRNA_min, miRNA_max, "
             "miRNA_end_5, miRNA_end_3, structure, homogeneity, miRBase_link, "
             "active_strand FROM backbone WHERE miRNA_s LIKE %s;")

    return get_multirow_by_query(query, (letters.upper() + "%",))


def serialize(name, flanks3_s, flanks3_a, flanks5_s, flanks5_a, loop_s,
              loop_a, miRNA_s, miRNA_a, miRNA_length, miRNA_min, miRNA_max,
              miRNA_end_5, miRNA_end_3, structure, homogeneity, miRBase_link,
              active_strand):
    """
    Function which serialize data from database to dictionary
    """
    return {
        'name': name,
        'flanks3_s': flanks3_s,
        'flanks3_a': flanks3_a,
        'flanks5_s': flanks5_s,
        'flanks5_a': flanks5_a,
        'loop_s': loop_s,
        'loop_a': loop_a,
        'miRNA_s': miRNA_s,
        'miRNA_a': miRNA_a,
        'miRNA_length': miRNA_length,
        'miRNA_min': miRNA_min,
        'miRNA_max': miRNA_max,
        'miRNA_end_5': miRNA_end_5,
        'miRNA_end_3': miRNA_end_3,
        'structure': structure,
        'homogeneity': homogeneity,
        'miRBase_link': miRBase_link,
        'active_strand': active_strand
    }


def serialize_immuno(sequence, receptor, link):
    """
    Function which serialize data from immuno table to dictionary
    """
    return {
        'sequence': sequence,
        'receptor': receptor,
        'link': link
    }
