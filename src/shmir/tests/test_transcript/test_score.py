import unittest
from mock import (
    patch,
    MagicMock
)

from shmir.designer.transcript import score


class TestScores(unittest.TestCase):

    def test_score_offset_positive_number(self):
        result = score.score_offtarget(10)
        self.assertEqual(result, 20)

    def test_score_offset_negative_number(self):
        result = score.score_offtarget(22)
        self.assertEqual(result, 0)

    def test_score_regexp(self):
        result = score.score_regexp(5)
        self.assertEqual(result, 25)

    @patch('shmir.designer.transcript.score.score_structure')
    def test_score_from_transcript(self, mock_structure):
        mock_structure.return_value = 10
        mock_frame = MagicMock(siRNA1='acgt')
        offtarget = 5
        regexp = 5
        result = score.score_from_transcript(
            mock_frame, 'original_frame', 'frame_ss', offtarget, regexp
        )
        self.assertEqual(result['structure'], mock_structure())
        self.assertEqual(result['offtarget'], 30)
        self.assertEqual(result['regexp'], 25)
        self.assertEqual(
            result['all'],
            mock_structure() + 30 + 25
        )
