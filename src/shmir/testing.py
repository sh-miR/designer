"""
.. module:: shmir.testing
    :synopsis: Module to help testing
"""

import os
import unittest

import mock
from sqlalchemy import create_engine
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker
)

from shmir.data import models


class TestModelBase(unittest.TestCase):

    def setUp(self):
        engine_uri_base = \
            'postgresql+psycopg2://postgres@{}:5432/'.format(
                os.environ.get('DB_PORT_5432_TCP_ADDR')
            )
        engine_uri_postgres = engine_uri_base + 'postgres'
        self.engine_postgres = create_engine(engine_uri_postgres)
        conn = self.engine_postgres.connect()
        conn.execute('commit;')
        try:
            conn.execute('create database shmird_test;')
        except:
            pass
        conn.close()

        engine_uri = engine_uri_base + 'shmird_test'

        self.engine = create_engine(engine_uri)
        self.db_session = scoped_session(sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        ))
        models.Base.metadata.drop_all(self.engine)
        models.Base.metadata.create_all(self.engine)

        self.db_patcher = \
            mock.patch('sqlalchemy.ext.declarative.declarative_base')
        self.db_patcher.start()

    def tearDown(self):
        models.Base.metadata.drop_all(self.engine_postgres)

        self.engine.dispose()
        self.engine_postgres.dispose()

        self.db_patcher.stop()

    def put_to_db(self, obj):
        self.db_session.add(obj)
        self.db_session.commit()

    def get_all(self, model):
        return self.db_session.query(model).all()


def create_backbone():
    """
    Function to create default backbone object
    """

    return models.Backbone(
        id=999,
        name='test_name',
        flanks3_s='test_flanks3_s',
        flanks3_a='test_flanks3_a',
        flanks5_s='test_flanks5_s',
        flanks5_a='test_flanks5_s',
        loop_s='test_loop_s',
        loop_a='test_loop_a',
        miRNA_s='test_miRNA_s',
        miRNA_a='test_miRNA_a',
        miRNA_length=23,
        miRNA_min=1,
        miRNA_max=69,
        miRNA_end_5=21,
        miRNA_end_3=32,
        structure='test_structure',
        homogeneity=32,
        miRBase_link='test_miRBase_link',
        active_strand=44,
        siRNA1='test_siRNA1',
        siRNA2='test_siRNA2'
    )
