from sqlalchemy import (
    Column,
    Integer
)

from shmir.data import models
from shmir.testing import (
    create_backbone,
    TestModelBase
)


class TestModelBaseCase(TestModelBase):

    class TestModel(models.Base):
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
