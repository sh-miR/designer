import unittest

from shmir.designer import errors
from shmir.designer.sirna import validators


class TestComplementarity(unittest.TestCase):

    def test_complementarity_level_max(self):
        seq1 = 'acggcttGGaacttctggtac'
        seq2 = 'gtaccagaagttccaagccgt'
        result = validators.complementarity_level(seq1, seq2)
        self.assertEqual(result, 100)

    def test_complementarity_level_incomplete(self):
        seq1 = 'acggcttggAActuctggtac'
        seq2 = 'gtaccagaacttaaaagccgt'
        result = validators.complementarity_level(seq1, seq2)
        self.assertEqual(result, 85)

    def test_best_complementarity_case1(self):
        seq1 = 'acggcttGGaactuctggtac'
        seq2 = 'gtaccagaagttccaagccgt'
        result = validators.best_complementarity(seq1, seq2)
        self.assertEqual(
            result,
            (seq1, seq2, 0, 0)  # new result
        )

    def test_best_complementarity_case2(self):
        seq1 = 'cttggaacttctggtacat'
        seq2 = 'gtaccagaagttccaagccgt'
        result = validators.best_complementarity(seq1, seq2)
        self.assertEqual(
            result,
            (seq1, seq2, -4, 2)
        )

    def test_best_complementarity_case3(self):
        seq1 = 'cttggaacttctggtacat'
        seq2 = 'tgtaccagaagttccaagccg'
        result = validators.best_complementarity(seq1, seq2)
        self.assertEqual(
            result,
            ('cttggaacttctggtacat', 'tgtaccagaagttccaagccg', -3, 1)
        )

    def test_best_complementarity_case4(self):
        seq1 = 'cttggaacttctggtacat'
        seq2 = 'gtaccagaagttccaagccgt'
        result = validators.best_complementarity(seq1, seq2)
        self.assertEqual(
            result,
            ('cttggaacttctggtacat', 'gtaccagaagttccaagccgt', -4, 2)
        )

    def test_best_complementarity_case5(self):
        seq1 = 'cttggaacttctggtacat'
        seq2 = 'tgtaccagaagttccaagccg'
        result = validators.best_complementarity(seq1, seq2)
        self.assertEqual(
            result,
            ('cttggaacttctggtacat', 'tgtaccagaagttccaagccg', -3, 1)
        )

    def test_best_complementarity_case6(self):
        seq1 = 'cttggaacttctggtacata'
        seq2 = 'tgtaccagaagttccaagccg'
        result = validators.best_complementarity(seq1, seq2)
        self.assertEqual(
            result,
            ('cttggaacttctggtacata', 'tgtaccagaagttccaagccg', -3, 2)
        )

    def test_best_complementarity_case7(self):
        seq1 = 'cttggaacttctggtacatag'
        seq2 = 'gtaccagaagttccaagcc'
        result = validators.best_complementarity(seq1, seq2)
        self.assertEqual(
            result,
            ('cttggaacttctggtacatag', 'gtaccagaagttccaagcc', -2, 4)
        )

    def test_best_complementarity_case8(self):
        seq1 = 'cttggaacttctggtacatag'
        seq2 = 'tgtaccagaagttccaagcc'
        result = validators.best_complementarity(seq1, seq2)
        self.assertEqual(
            result,
            ('cttggaacttctggtacatag', 'tgtaccagaagttccaagcc', -2, 3)
        )

    def test_best_complementarity_case9(self):
        seq1 = 'cttggaacttctggtacatag'
        seq2 = 'tagtaccagaagttccaagcc'
        result = validators.best_complementarity(seq1, seq2)
        self.assertEqual(
            result,
            ('cttggaacttctggtacatag', 'tagtaccagaagttccaagcc', -2, 2)
        )

    def test_best_complementarity_case10(self):
        seq1 = 'cttggaacttctggtacata'
        seq2 = 'tagtaccagaagttccaagcc'
        result = validators.best_complementarity(seq1, seq2)
        self.assertEqual(
            result,
            ('cttggaacttctggtacata', 'tagtaccagaagttccaagcc', -2, 1)
        )

    def test_best_complementarity_case11(self):
        seq1 = 'cttggaacttctggtacat'
        seq2 = 'tagtaccagaagttccaagcc'
        result = validators.best_complementarity(seq1, seq2)
        self.assertEqual(
            result,
            ('cttggaacttctggtacat', 'tagtaccagaagttccaagcc', -2, 0)
        )

    def test_best_complementarity_case12(self):
        seq1 = 'cttggaacttctggtacatgc'
        seq2 = 'tgtaccagaagttccaagc'
        result = validators.best_complementarity(seq1, seq2)
        self.assertEqual(
            result,
            ('cttggaacttctggtacatgc', 'tgtaccagaagttccaagc', -1, 3)
        )

    def test_best_complementarity_case13(self):
        seq1 = 'cttggaacttctggtacatg'
        seq2 = 'tgtaccagaagttccaagc'
        result = validators.best_complementarity(seq1, seq2)
        self.assertEqual(
            result,
            ('cttggaacttctggtacatg', 'tgtaccagaagttccaagc', -1, 2)
        )

    def test_best_complementarity_case14(self):
        seq1 = 'cttggaacttctggtacat'
        seq2 = 'tgtaccagaagttccaagc'
        result = validators.best_complementarity(seq1, seq2)
        self.assertEqual(
            result,
            ('cttggaacttctggtacat', 'tgtaccagaagttccaagc', -1, 1)
        )

    def test_best_complementarity_case15(self):
        seq1 = 'cttggaacttctggtacat'
        seq2 = 'atgtaccagaagttccaagc'
        result = validators.best_complementarity(seq1, seq2)
        self.assertEqual(
            result,
            ('cttggaacttctggtacat', 'atgtaccagaagttccaagc', -1, 0)
        )

    def test_best_complementarity_case16(self):
        seq1 = 'cttggaacttctggtacat'
        seq2 = 'catgtaccagaagttccaagc'
        result = validators.best_complementarity(seq1, seq2)
        self.assertEqual(
            result,
            ('cttggaacttctggtacat', 'catgtaccagaagttccaagc', -1, -1)
        )

    def test_best_complementarity_case17(self):
        seq1 = 'acggcttggaacttctggtac'
        seq2 = 'accagaagttccaagccgt'
        result = validators.best_complementarity(seq1, seq2)
        self.assertEqual(
            result,
            ('acggcttggaacttctggtac', 'accagaagttccaagccgt', 0, 2)
        )

    def test_best_complementarity_case18(self):
        seq1 = 'acggcttggaacttctggtac'
        seq2 = 'taccagaagttccaagccgt'
        result = validators.best_complementarity(seq1, seq2)
        self.assertEqual(
            result,
            ('acggcttggaacttctggtac', 'taccagaagttccaagccgt', 0, 1)
        )

    def test_best_complementarity_case19(self):
        seq1 = 'acggcttggaacttctggtac'
        seq2 = 'gtaccagaagttccaagccgt'
        result = validators.best_complementarity(seq1, seq2)
        self.assertEqual(
            result,
            ('acggcttggaacttctggtac', 'gtaccagaagttccaagccgt', 0, 0)
        )

    def test_best_complementarity_case20(self):
        seq1 = 'acggcttggaacttctggta'
        seq2 = 'gtaccagaagttccaagccgt'
        result = validators.best_complementarity(seq1, seq2)
        self.assertEqual(
            result,
            ('acggcttggaacttctggta', 'gtaccagaagttccaagccgt', 0, -1)
        )

    def test_best_complementarity_case21(self):
        seq1 = 'acggcttggaacttctggt'
        seq2 = 'gtaccagaagttccaagccgt'
        result = validators.best_complementarity(seq1, seq2)
        self.assertEqual(
            result,
            ('acggcttggaacttctggt', 'gtaccagaagttccaagccgt', 0, -2)
        )

    def test_best_complementarity_case22(self):
        seq1 = 'acggcttggaacttctggtac'
        seq2 = 'taccagaagttccaagccg'
        result = validators.best_complementarity(seq1, seq2)
        self.assertEqual(
            result,
            ('acggcttggaacttctggtac', 'taccagaagttccaagccg', 1, 1)
        )

    def test_best_complementarity_case23(self):
        seq1 = 'acggcttggaacttctggtac'
        seq2 = 'gtaccagaagttccaagccg'
        result = validators.best_complementarity(seq1, seq2)
        self.assertEqual(
            result,
            ('acggcttggaacttctggtac', 'gtaccagaagttccaagccg', 1, 0)
        )

    def test_best_complementarity_case24(self):
        seq1 = 'acggcttggaacttctggta'
        seq2 = 'gtaccagaagttccaagccg'
        result = validators.best_complementarity(seq1, seq2)
        self.assertEqual(
            result,
            ('acggcttggaacttctggta', 'gtaccagaagttccaagccg', 1, -1)
        )

    def test_best_complementarity_case25(self):
        seq1 = 'acggcttggaacttctggt'
        seq2 = 'gtaccagaagttccaagccg'
        result = validators.best_complementarity(seq1, seq2)
        self.assertEqual(
            result,
            ('acggcttggaacttctggt', 'gtaccagaagttccaagccg', 1, -2)
        )

    def test_best_complementarity_case26(self):
        seq1 = 'acggcttggaacttctggt'
        seq2 = 'agtaccagaagttccaagccg'
        result = validators.best_complementarity(seq1, seq2)
        self.assertEqual(
            result,
            ('acggcttggaacttctggt', 'agtaccagaagttccaagccg', 1, -3)
        )

    def test_best_complementarity_case27(self):
        seq1 = 'acggcttggaacttctggtac'
        seq2 = 'gtaccagaagttccaagcc'
        result = validators.best_complementarity(seq1, seq2)
        self.assertEqual(
            result,
            ('acggcttggaacttctggtac', 'gtaccagaagttccaagcc', 2, 0)
        )

    def test_best_complementarity_case28(self):
        seq1 = 'acggcttggaacttctggta'
        seq2 = 'gtaccagaagttccaagcc'
        result = validators.best_complementarity(seq1, seq2)
        self.assertEqual(
            result,
            ('acggcttggaacttctggta', 'gtaccagaagttccaagcc', 2, -1)
        )

    def test_best_complementarity_case29(self):
        seq1 = 'acggcttggaacttctggt'
        seq2 = 'gtaccagaagttccaagcc'
        result = validators.best_complementarity(seq1, seq2)
        self.assertEqual(
            result,
            ('acggcttggaacttctggt', 'gtaccagaagttccaagcc', 2, -2)
        )

    def test_best_complementarity_case30(self):
        seq1 = 'acggcttggaacttctggt'
        seq2 = 'agtaccagaagttccaagcc'
        result = validators.best_complementarity(seq1, seq2)
        self.assertEqual(
            result,
            ('acggcttggaacttctggt', 'agtaccagaagttccaagcc', 2, -3)
        )

    def test_best_complementarity_case31(self):
        seq1 = 'acggcttggaacttctggt'
        seq2 = 'gagtaccagaagttccaagcc'
        result = validators.best_complementarity(seq1, seq2)
        self.assertEqual(
            result,
            ('acggcttggaacttctggt', 'gagtaccagaagttccaagcc', 2, -4)
        )

    def test_best_complementarity_case32(self):
        seq1 = 'cacggcttggaacttctggta'
        seq2 = 'gtaccagaagttccaagcc'
        result = validators.best_complementarity(seq1, seq2)
        self.assertEqual(
            result,
            ('cacggcttggaacttctggta', 'gtaccagaagttccaagcc', 3, -1)
        )

    def test_best_complementarity_case33(self):
        seq1 = 'cacggcttggaacttctggt'
        seq2 = 'gtaccagaagttccaagcc'
        result = validators.best_complementarity(seq1, seq2)
        self.assertEqual(
            result,
            ('cacggcttggaacttctggt', 'gtaccagaagttccaagcc', 3, -2)
        )

    def test_best_complementarity_case34(self):
        seq1 = 'gcacggcttggaacttctggt'
        seq2 = 'gtaccagaagttccaagcc'
        result = validators.best_complementarity(seq1, seq2)
        self.assertEqual(
            result,
            ('gcacggcttggaacttctggt', 'gtaccagaagttccaagcc', 4, -2)
        )


class TestReplaceModules(unittest.TestCase):

    def test_replace_mocules(self):
        input_seq = 'aCuAT'
        output_seq = 'ACTAT'
        self.assertEqual(validators.replace_mocules(input_seq), output_seq)

    def test_replace_mocules_with_cut(self):
        input_seq = 'aCuATT'
        output_seq = 'ACTA'
        self.assertEqual(validators.replace_mocules(input_seq), output_seq)


class TestValidateSirna(unittest.TestCase):

    def test_validate_sirna(self):
        seq = 'ACGTACGTACGTACGTACGT'
        self.assertIsNone(validators.validate_sirna(seq))

    def test_validate_sirna_incorrect_length(self):
        incorrect_seq = 'ACGT'
        with self.assertRaises(errors.ValidationError) as error:
            validators.validate_sirna(incorrect_seq)
        self.assertEqual(error.exception.message, errors.LENGTH_ERROR)

    def test_validate_sirna_incorrect_pattern(self):
        incorrect_seq = 'ptaki lataja kluczem'
        with self.assertRaises(errors.ValidationError) as error:
            validators.validate_sirna(incorrect_seq)
        self.assertEqual(error.exception.message, errors.PATTERN_ERROR)


class TestParseInput(unittest.TestCase):

    def test_parse_input(self):
        correct_seq = 'cttggaacttctggtacat gtaccagaagttccaagccgt'
        result = validators.parse_input(correct_seq)
        self.assertEqual(
            result,
            ('CTTGGAACTTCTGGTACAT', 'GTACCAGAAGTTCCAAGCCGT', -4, 2)
        )

    @unittest.skip('Return any code')
    def test_parse_input_invalid_response(self):
        incorrect_seq = 'ptaki lataja kluczem'
        result = validators.parse_input(incorrect_seq)
        self.assertEqual(result['status'], 'error')
        self.assertEqual(result['code'], 400)

    def test_parse_input_correct(self):
        correct_seq = 'cttggaacttctggtacat gtaccagaagttccaagccgt'
        result = validators.parse_input(correct_seq)
        self.assertEqual(
            result,
            ('CTTGGAACTTCTGGTACAT', 'GTACCAGAAGTTCCAAGCCGT', -4, 2)
        )
