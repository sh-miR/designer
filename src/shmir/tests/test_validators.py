import unittest

from shmir.designer.validators import (
    calculate_gc_content,
    validate_gc_content,
)


class TestValidators(unittest.TestCase):

    def test_calculate_gc_content(self):
        seq_percent = calculate_gc_content('ACGT')
        self.assertEqual(seq_percent, 50)

        seq_percent = calculate_gc_content('CCCCGGGG')
        self.assertEqual(seq_percent, 100)

        seq_percent = calculate_gc_content('ACTTTTTTTA')
        self.assertEqual(seq_percent, 10)

    def test_validate_gc_content(self):
        is_in_range = validate_gc_content('ACGT', 40, 60)
        self.assertTrue(is_in_range)

    def test_validate_gc_content_not_in_range(self):
        not_in_range = validate_gc_content('ACGT', 52, 70)
        self.assertFalse(not_in_range)
