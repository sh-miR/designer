from mock import MagicMock
import unittest

from shmir.designer.transcript.worker import (
    shmir_from_fasta,
)


class TestScores(unittest.TestCase):

    def test_shmir_from_fasta(self):
        sirna = "AAAGGGGCTTTTagtcttaga"
        offtarget = "NC_12345"
        regex = "*"
        original_frames = MagicMock()
        results = shmir_from_fasta(
            sirna, offtarget, regex, original_frames, 'aa'
        )
        self.assertEqual(results, [])
