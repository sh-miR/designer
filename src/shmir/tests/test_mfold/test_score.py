import unittest
from mock import (
    patch,
    MagicMock
)

from shmir.designer.mfold.score import score_structure


class TestScore(unittest.TestCase):

    @patch('shmir.designer.mfold.score.parse_score')
    @patch('shmir.designer.mfold.score.parse_ss')
    def test_score_structure(self, mock_parse_ss, mock_parse_score):
        mock_parse_ss.return_value = 'acgtacgt'
        mock_parse_score.return_value = 4.0, [('a', 1), ('c', 4)]
        frame = MagicMock()
        original_frame = MagicMock()
        original_frame.flanks5_s = 'acgt'
        original_frame.miRNA_s = 'cgta'
        original_frame.loop_s = 'aacc'
        original_frame.flanks3_s = 'acg'
        original_frame.miRNA_a = 'aa'

        frame.flanks5_s = 'acg'
        frame.siRNA1 = 'ac'
        frame.loop_s = 'a'
        frame.siRNA2 = 'c'
        frame.flanks3_s = 'a'
        result = score_structure(frame, 'folding_file', original_frame)

        self.assertEqual(result, 250)
