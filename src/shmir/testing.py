"""
.. module:: shmir.testing
    :synopsis: Module to help testing
"""

import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker
)

from shmir.data import models


class TestModelBase(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        self.db_session = scoped_session(sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        ))
        models.Base.metadata.create_all(bind=self.engine)

    def tearDown(self):
        self.engine.dispose()

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
    )
