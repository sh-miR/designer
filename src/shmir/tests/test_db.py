from sqlalchemy import (
    Column,
    Integer
)

from shmir.data import models
from shmir.testing import (
    create_backbone,
    TestModelBase
)

from shmir.designer.utils import (
    adjusted_frames,
    reverse_complement
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
        template = backbone.template()
        self.assertEqual(
            template,
            ''.join(
                ['test_flanks5_s', 'test_siRNA1',
                 'test_loop_s', 'test_siRNA2', 'test_flanks3_s']
            ).upper()
        )

    def test_reverse_complement(self):
        sequence = "atcgatcg"
        reversed_sequence = "cgatcgat"
        result = reverse_complement(sequence)
        self.assertEqual(result, reversed_sequence)

    def test_adjusted_frames(self):
        seq1 = 'acgt'
        seq2 = 'gtac'
        shift_left = 0
        shift_right = 0
        backbone = create_backbone()
        backbone.active_strand = 3
        all_frames = [backbone]
        results = adjusted_frames(
            seq1, seq2, shift_left, shift_right, all_frames
        )
        self.assertEqual(all_frames, results)
