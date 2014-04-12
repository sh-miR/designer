import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from testing import create_backbone, TestModelBase
from sqlalchemy import Column, Integer
import settings


class TestModelBaseCase(TestModelBase):

    class TestModel(settings.Base):
        __tablename__ = 'test_table'

        id = Column(Integer, primary_key=True)

    def test_get_and_put_to_db(self):
        new_obj = self.TestModel(id=153)
        self.put_to_db(new_obj)
        objs = self.get_all(self.TestModel)

        self.assertEqual(len(objs), 1)


class TestBackboneModel(TestModelBase):

    def test_template(self):
        backbone = create_backbone()
        template = backbone.template('strand1', 'strand2')
        self.assertEqual(
            template,
            ''.join(
                ['test_flanks5_s', 'strand1',
                 'test_loop_s', 'strand2', 'test_flanks3_s']
            ).upper()
        )
