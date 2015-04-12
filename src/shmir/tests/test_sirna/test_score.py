import unittest
from mock import (
    MagicMock,
    patch
)

from shmir.designer.sirna import score


class TestScore(unittest.TestCase):

    def test_score_homogenity(self):
        homogeneity = 12
        mock_frame = MagicMock(homogeneity=homogeneity)
        score_result = score.score_homogeneity(mock_frame)
        self.assertEqual(score_result, homogeneity*3)

    def test_score_two_same_strands_two_matches(self):
        mock_original_frame = MagicMock(miRNA_s='actg')
        seq = 'acgt'
        result = score.score_two_same_strands(seq, mock_original_frame)
        self.assertEqual(result, 10)

    def test_score_two_same_strands_one_matches(self):
        mock_original_frame = MagicMock(miRNA_s='attg')
        seq = 'acgt'
        result = score.score_two_same_strands(seq, mock_original_frame)
        self.assertEqual(result, 4)

    def test_score_two_same_strands_zero_matches(self):
        mock_original_frame = MagicMock(miRNA_s='attg')
        seq = 'ccgt'
        result = score.score_two_same_strands(seq, mock_original_frame)
        self.assertEqual(result, 0)

    @patch('shmir.designer.sirna.score.score_structure')
    @patch('shmir.designer.sirna.score.score_two_same_strands')
    @patch('shmir.designer.sirna.score.score_homogeneity')
    def test_score_from_sirna(
        self, mock_homogeneity, mock_same_ends, mock_structure
    ):
        mock_structure.return_value = 10
        mock_homogeneity.return_value = 11
        mock_same_ends.return_value = 12
        mock_frame = MagicMock(siRNA1='acgt')

        result = score.score_from_sirna(mock_frame, 'original_frame', 'file')
        self.assertEqual(result['structure'], mock_structure())
        self.assertEqual(result['homogeneity'], mock_homogeneity())
        self.assertEqual(result['same_ends'], mock_same_ends())
        self.assertEqual(
            result['all'],
            mock_structure() + mock_homogeneity() + mock_same_ends()
        )
