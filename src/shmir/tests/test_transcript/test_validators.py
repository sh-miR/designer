import unittest
from shmir.testing import TestModelBase

from shmir.designer.transcript import validators


class TestValidators(unittest.TestCase):

    def setUp(self):
        super(TestValidators, self).setUp()

    def test_calculate_gc_content(self):
        seq_percent = validators.calculate_gc_content('ACGT')
        self.assertEqual(seq_percent, 50)

        seq_percent = validators.calculate_gc_content('CCCCGGGG')
        self.assertEqual(seq_percent, 100)

        seq_percent = validators.calculate_gc_content('ACTTTTTTTA')
        self.assertEqual(seq_percent, 10)

    def test_validate_gc_content(self):
        is_in_range = validators.validate_gc_content('ACGT', 40, 60)
        self.assertTrue(is_in_range)

    def test_validate_gc_content_not_in_range(self):
        not_in_range = validators.validate_gc_content('ACGT', 52, 70)
        self.assertFalse(not_in_range)

    def test_validate_immuno_no_difference(self):
        self.assertTrue(validators.validate_immuno('aaa', 'no_difference'))

    # def test_validate_immuno(self):
    #     from shmir.data.models import Immuno
    #     self.put_to_db(Immuno())
    #     #need to investigate problem with db

    def test_validate_transcript_by_score_false(self):
        score = {'structure': 70, 'all': 80}
        self.assertFalse(validators.validate_transcript_by_score(score))

    def test_validate_transcript_by_score_true(self):
        score = {'structure': 70, 'all': 101}
        self.assertTrue(validators.validate_transcript_by_score(score))
