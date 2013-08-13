#!/usr/bin/python
#

"""
Test for shmiR application
"""

import unittest
import utils

class ShmiRTest(unittest.TestCase):
    
    def test_input(self):
        tests = [
            ('acggctTggaacttctggtac', ['acggcttggaacttctggtac']),
            ('acggcttGGaacttctggtac gtaccagaagttccaagccgt', [utils.check_complementary('acggcttggaacttctggtac', 'gtaccagaagttccaagccgt')]),
            ('acggcttggAActuctggtac gtaccagaagttccaagccgt', [utils.check_complementary('acggcttggaacttctggtac', 'gtaccagaagttccaagccgt')]),
            ('acggctTggaacttctggtTT', ['acggcttggaacttctggt']),
            ]
        for list1, expected in tests:
            self.failUnlessEqual(utils.check_input(list1), expected) 

    """def test_input_exceptions(self):
        self.assertRaisesWithMessage(utils.check_input('acggcttggaactuct'), InputException('to long or to short'))
        self.assertRaisesWithMessage(utils.check_input(''), InputException('to long or to short'))
        self.assertRaisesWithMessage(utils.check_input('acttctggtacTTUUUUUUuuuuuuGGG'), InputException('to long or to short'))
        self.assertRaisesWithMessage(utils.check_input('acggcttGGaacttctggtac gtaccagaagttccaagccgt acggcttGGaacttctggtac'), InputException('insert only one siRNA sequence or both strands of one siRNA at a time; check if both stands are in 5-3 orientation'))
        self.assertRaisesWithMessage(utils.check_input('acggcttGGaacttctggtac tgccgaaccttgaagaccatg'), InputException('insert only one siRNA sequence or both strands of one siRNA at a time; check if both stands are in 5-3 orientation'))
        self.assertRaisesWithMessage(utils.check_input('acggctTggaacttctggtwacTT'), InputException('sequence can contain only {actgu} letters'))"""
    
    def test_check_complementary(self):
        tests = [
            ('cttggaacttctggtacat', 'gtaccagaagttccaagccgt', ('cttggaacttctggtacat', 'gtaccagaagttccaagccgt', -4, 2)),

            ('cttggaacttctggtacat', 'tgtaccagaagttccaagccg', ('cttggaacttctggtacat', 'tgtaccagaagttccaagccg', -3, 1)),
            ('cttggaacttctggtacata', 'tgtaccagaagttccaagccg', ('cttggaacttctggtacata', 'tgtaccagaagttccaagccg', -3, 2)),

            ('cttggaacttctggtacatag', 'gtaccagaagttccaagcc', ('cttggaacttctggtacatag', 'gtaccagaagttccaagcc', -2, 4)),
            ('cttggaacttctggtacatag', 'tgtaccagaagttccaagcc', ('cttggaacttctggtacatag', 'tgtaccagaagttccaagcc', -2, 3)),
            ('cttggaacttctggtacatag', 'tagtaccagaagttccaagcc', ('cttggaacttctggtacatag', 'tagtaccagaagttccaagcc', -2, 2)),
            ('cttggaacttctggtacata', 'tagtaccagaagttccaagcc', ('cttggaacttctggtacata', 'tagtaccagaagttccaagcc', -2, 1)),
            ('cttggaacttctggtacat', 'tagtaccagaagttccaagcc', ('cttggaacttctggtacat', 'tagtaccagaagttccaagcc', -2, 0)),

            ('cttggaacttctggtacatgc', 'tgtaccagaagttccaagc', ('cttggaacttctggtacatgc', 'tgtaccagaagttccaagc', -1, 3)),
            ('cttggaacttctggtacatg', 'tgtaccagaagttccaagc', ('cttggaacttctggtacatg', 'tgtaccagaagttccaagc', -1, 2)),
            ('cttggaacttctggtacat', 'tgtaccagaagttccaagc', ('cttggaacttctggtacat', 'tgtaccagaagttccaagc', -1, 1)),
            ('cttggaacttctggtacat', 'atgtaccagaagttccaagc', ('cttggaacttctggtacat', 'atgtaccagaagttccaagc', -1, 0)),
            ('cttggaacttctggtacat', 'catgtaccagaagttccaagc', ('cttggaacttctggtacat', 'catgtaccagaagttccaagc' -1, -1)),


            ('acggcttggaacttctggtac', 'accagaagttccaagccgt', ('acggcttggaacttctggtac', 'accagaagttccaagccgt', 0, 2)),
            ('acggcttggaacttctggtac', 'taccagaagttccaagccgt', ('acggcttggaacttctggtac', 'taccagaagttccaagccgt', 0, 1)),
            ('acggcttggaacttctggtac', 'gtaccagaagttccaagccgt', ('acggcttggaacttctggtac', 'gtaccagaagttccaagccgt', 0, 0)),
            ('acggcttggaacttctggta', 'gtaccagaagttccaagccgt', ('acggcttggaacttctggta', 'gtaccagaagttccaagccgt', 0, -1)),
            ('acggcttggaacttctggt', 'gtaccagaagttccaagccgt', ('acggcttggaacttctggt', 'gtaccagaagttccaagccgt', 0, -2)),


            ('acggcttggaacttctggtac', 'taccagaagttccaagccg', ('acggcttggaacttctggtac', 'taccagaagttccaagccg', 1, 1)),
            ('acggcttggaacttctggtac', 'gtaccagaagttccaagccg', ('acggcttggaacttctggtac', 'gtaccagaagttccaagccg', 1, 0)),
            ('acggcttggaacttctggta', 'gtaccagaagttccaagccg', ('acggcttggaacttctggta', 'gtaccagaagttccaagccg', 1, -1)),
            ('acggcttggaacttctggt', 'gtaccagaagttccaagccg', ('acggcttggaacttctggt', 'gtaccagaagttccaagccg', 1, -2)),
            ('acggcttggaacttctggt', 'agtaccagaagttccaagccg', ('acggcttggaacttctggt', 'agtaccagaagttccaagccg', 1, -3)),

            ('acggcttggaacttctggtac', 'gtaccagaagttccaagcc', ('acggcttggaacttctggtac', 'gtaccagaagttccaagcc', 2, 0)),
            ('acggcttggaacttctggta', 'gtaccagaagttccaagcc', ('acggcttggaacttctggta', 'gtaccagaagttccaagcc', 2, -1)),
            ('acggcttggaacttctggt', 'gtaccagaagttccaagcc', ('acggcttggaacttctggt', 'gtaccagaagttccaagcc', 2, -2)),
            ('acggcttggaacttctggt', 'agtaccagaagttccaagcc', ('acggcttggaacttctggt', 'agtaccagaagttccaagcc', 2, -3)),
            ('acggcttggaacttctggt', 'gagtaccagaagttccaagcc', ('acggcttggaacttctggt', 'gagtaccagaagttccaagcc', 2, -4)),

            ('cacggcttggaacttctggta', 'gtaccagaagttccaagcc', ('cacggcttggaacttctggta', 'gtaccagaagttccaagcc', 3, -1)),
            ('cacggcttggaacttctggt', 'gtaccagaagttccaagcc', ('cacggcttggaacttctggt', 'gtaccagaagttccaagcc', 3, -2)),

            ('gcacggcttggaacttctggt', 'gtaccagaagttccaagcc', ('gcacggcttggaacttctggt', 'gtaccagaagttccaagcc', 4, -2))
            ]
        for seq1, seq2, expected in tests:
            self.failUnlessEqual(utils.check_complementary(seq1, seq2), expected)

    """def test_complementary_exceptions(self):
        self.assertRaisesWithMessage(utils.check_complementary('acggcttGGaacttctggtac', 'gaaggtgaagccccaagccgt'), InputException('>20% mismaches'))
        self.assertRaisesWithMessage(utils.check_complementary('acggcttGGaacttctggtac', 'gtaccagaagttccaagccgttua'), InputException('+3'))
        self.assertRaisesWithMessage(utils.check_complementary('acggcttggAActuctggtac', 'acggcttggAActuctggtac'), InputException('both same strands'))"""

    #def test_get_frames(self):

     #   tests = [
     #       ('', ()),
     #       ('', ())
     #       ]
     #   for sequences, expected in tests:
     #       self.failUnlessEqual(utils.get_frames(sequences), expected)


if __name__ == '__main__':
    unittest.main()
