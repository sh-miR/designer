"""
Module for communication with database
"""

from flask import g

from sqlsoup import SQLSoup
from sqlalchemy import func
from shmir_api.settings import DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT


def get_db():
    """
    Global connector variable
    """
    db = getattr(g, '_database', None)
    if db is None:
        conn_str = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
        fconn = conn_str.format(dbname=DB_NAME, user=DB_USER,
                                password=DB_PASS, host=DB_HOST, port=DB_PORT)
        db = g._database = SQLSoup(fconn)

    return db


def disconnect():
    """
    Global disconnector
    """
    db = getattr(g, '_database', None)
    if db is not None:
        db.connection().close()


def serialized_all_by_query(query, serialize):
    """
    Function which returns serialized query, serialize is a function
    """
    return [serialize(elem) for elem in query.all()]


def backbone_get_all():
    """
    Function which gets all serialized Backbones in database
    """
    db = get_db()
    return serialized_all_by_query(db.backbone, backbone_serialize)


def backbone_get_by_name(name):
    """
    Function which gets one serialized Backbone by name
    """
    db = get_db()
    data = db.backbone.filter(func.lower(db.backbone.name) ==
                              func.lower(name)).first()

    return backbone_serialize(data) if data else {}


def backbone_get_by_miRNA_s(letters):
    """
    Function which gets serialized Backbones having first two letters of
    miRNA_s same as letters given (first two nucleotides of siRNA strand)
    """
    db = get_db()
    query = db.backbone.filter(db.backbone.mirna_s.
                               like("{}%".format(letters.upper())))

    return serialized_all_by_query(query, backbone_serialize)


def immuno_get_all():
    """
    Function which gets all serialized immuno sequences in database
    """
    db = get_db()
    return serialized_all_by_query(db.immuno, immuno_serialize)


def backbone_serialize(obj):
    """
    Function which serialize backbone data from database to dictionary
    """
    return {
        'name': obj.name,
        'flanks3_s': obj.flanks3_s,
        'flanks3_a': obj.flanks3_a,
        'flanks5_s': obj.flanks5_s,
        'flanks5_a': obj.flanks5_a,
        'loop_s': obj.loop_s,
        'loop_a': obj.loop_a,
        'miRNA_s': obj.mirna_s,
        'miRNA_a': obj.mirna_a,
        'miRNA_length': obj.mirna_length,
        'miRNA_min': obj.mirna_min,
        'miRNA_max': obj.mirna_max,
        'miRNA_end_5': obj.mirna_end_5,
        'miRNA_end_3': obj.mirna_end_3,
        'structure': obj.structure,
        'homogeneity': obj.homogeneity,
        'miRBase_link': obj.mirbase_link,
        'active_strand': obj.active_strand
    }


def immuno_serialize(obj):
    """
    Function which serialize immuno data from immuno table to dictionary
    """
    return {
        'sequence': obj.sequence,
        'receptor': obj.receptor,
        'link': obj.link
    }
