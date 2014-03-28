#!/usr/bin/python

"""
Test for shmiR application
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from shmir_designer import validators
from shmir_designer import errors
from shmir_designer import search


class TestShmiR(unittest.TestCase):
    """Tests for shmiR designer application"""
    def test_input(self):
        """Tests for check_input function"""
        tests = [
            ('acggctTggaacttctggtac', ('acggcttggaacttctggtac', '', 0, 0)),
            ('acggcttGGaacttctggtac gtaccagaagttccaagccgt', (validators.check_complementary('acggcttggaacttctggtac', 'gtaccagaagttccaagccgt'))),
            ('acggcttggAActuctggtac gtaccagaagttccaagccgt', (validators.check_complementary('acggcttggaacttctggtac', 'gtaccagaagttccaagccgt'))),
            ('acggctTggaacttctggtTT', ('acggcttggaacttctggt', '', 0, 0))]
        for list1, expected in tests:
            self.failUnlessEqual(validators.check_input(list1), expected)

    def multiple_input(self, data, error):
        for strand in data:
            with self.assertRaises(errors.InputException) as err:
                validators.check_input(strand)
            self.assertEqual(error, str(err.exception))

    def test_input_exceptions(self):
        """Tests for check_input Exceptions"""
        len_data = ['acggcttggaactuct', '', 'acttctggtacTTUUUUUUuuuuuuGGG']
        error_data = ['acggcttGGaacttctggtac gtaccagaagttccaagccgt '
                      'acggcttGGaacttctggtac',
                      'acggcttGGaacttctggtac tgccgaaccttgaagaccatg']
        patt_data = ['acggctTggactggtwacTT']

        self.multiple_input(len_data, errors.len_error)
        self.multiple_input(error_data, errors.error)
        self.multiple_input(patt_data, errors.patt_error)

    def test_check_complementary(self):
        """Tests for check_complementary function"""
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
            ('cttggaacttctggtacat', 'catgtaccagaagttccaagc', ('cttggaacttctggtacat', 'catgtaccagaagttccaagc', -1, -1)),


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
            self.failUnlessEqual(validators.check_complementary(seq1, seq2), expected)



#    def test_create_regular(self):
#        """Tests for create_regular function"""
#        tests=[
#            ('UGUAAACAUCCUCGACUGGAAG', {1: [r'[UT][UAGC]{18}', r'[UT][UAGC]{19}', r'[UT][UAGC]{20}'],  
#            2: [r'[UT][UAGC]{17}[G]', r'[UT][UAGC]{18}[G]', r'[UT][UAGC]{19}[G]'
#            r'[UT][G][UAGC]{17}', r'[UT][G][UAGC]{18}', r'[UT][G][UAGC]{19}'],
#            3: [r'[UT][G][UAGC]{16}[G]', r'[UT][G][UAGC]{17}[G]', r'[UT][G][UAGC]{18}[G]'], 
#            4: [r'[UT][G][UAGC]{15}[A][G]', r'[UT][G][UAGC]{16}[A][G]', r'[UT][G][UAGC]{17}[A][G]']}),
#            ('CTTCCAGTCGAGGATGTTTGCAGC', {1:[r'[C][UAGC]{18}', r'[C][UAGC]{19}', r'[C][UAGC]{20}'], 
#            2: [r'[C][UAGC]{17}[C]', r'[C][UAGC]{18}[C]', r'[C][UAGC]{19}[C]',
#            r'[C][T][UAGC]{17}', r'[C][T][UAGC]{18}', r'[C][T][UAGC]{19}'], 
#            3: [r'[C][UT][UAGC]{16}[C]', r'[C][UT][UAGC]{17}[C]', r'[C][UT][UAGC]{18}[C]'], 
#            4: [r'[C][UT][UAGC]{15}[G][C]', r'[C][UT][UAGC]{16}[G][C]', r'[C][UT][UAGC]{17}[G][C]']}),
#            ('AGGCTTGCTGTAGGCTGTATGCTG', {1: [r'[A][UAGC]{18}', r'[A][UAGC]{19}', r'[A][UAGC]{20}'], 
#           2: [r'[A][UAGC]{19}[G]', r'[A][UAGC]{18}[G]', r'[A][UAGC]{19}[G]', 
#            r'[A][G][UAGC]{17}', r'[A][G][UAGC]{18}', r'[A][G][UAGC]{19}'], 
#            3: [r'[A][G][UAGC]{16}[G]', r'[A][G][UAGC]{17}[G]', r'[A][G][UAGC]{18}[G]'], 
#            4: [r'[A][G][UAGC]{15}[TU][G]', r'[A][G][UAGC]{16}[TU][G]', r'[A][G][UAGC]{17}[TU][G]']}),
#            ('UGGAGUGUGACAAUGGUGUUUG', {1: [r'[UT][UAGC]{18}', r'[UT][UAGC]{19}', r'[UT][UAGC]{20}'], 
#            2: [r'[UT][UAGC]{17}[G]', r'[UT][UAGC]{18}[G]', r'[UT][UAGC]{19}[G]', 
#            r'[UT][G][UAGC]{17}', r'[UT][G][UAGC]{18}', r'[UT][G][UAGC]{19}'], 
#            3: [r'[UT][G][UAGC]{16}[G]', r'[UT][G][UAGC]{17}[G]', r'[UT][G][UAGC]{18}[G]'], 
#            4: [r'[UT][G][UAGC]{15}[UT][G]', r'[UT][G][UAGC]{16}[UT][G]', r'[UT][G][UAGC]{17}[UT][G]']}),
#            ('AGGCAAGAUGCUGGCAUAGCU', {1: [r'[A][UAGC]{18}', r'[A][UAGC]{19}', r'[A][UAGC]{20}'], 
#            2: [r'[A][UAGC]{17}[UT]', r'[A][UAGC]{18}[UT]', r'[A][UAGC]{19}[UT]',
#            r'[A][G][UAGC]{17}', r'[A][G][UAGC]{18}', r'[A][G][UAGC]{19}'], 
#            3: [r'[A][G][UAGC]{16}[TU]', r'[A][G][UAGC]{17}[TU]', r'[A][G][UAGC]{18}[TU]'], 
#            4: [r'[A][G][UAGC]{15}[C][TU]', r'[A][G][UAGC]{16}[C][TU]', r'[A][G][UAGC]{17}[C][TU]']})
#       ]

#        for test in tests:
#            test[1].items().sort()
#            for k, v in test[1].iteritems():
#                v.sort()
#        for seq, expected in tests:
#            self.failUnlessEqual(search.create_regular(seq), expected)
            
            
    def test_find_regular(self):
        """Tests for finding regular expressions with importance number"""
        tests=[
        (search.find_by_patterns({2: [r'[A][G][TUAGC]{5}', r'[A][G][TUAGC]{6}']}, 'GCACTCGCCGCGAGGGTTGCCGGGACGGGCCCAAGATGGCTGGGAGCTTTGGTTCCGCTTCGGTCTACCTCGTAGAGCCCCATTCATTACCTTGC'),
        {2 : ['AGGGTTG', 'AGGGTTGC', 'AGATGGC', 'AGATGGCT', 'AGCTTTG', 'AGCTTTGG', 'AGAGCCC', 'AGAGCCCC', 'AGCCCCA', 'AGCCCCAT']}),
        (search.find_by_patterns({2: [r'[A][TUAGC]{5}[G]', r'[A][TUAGC]{6}[G]']}, 'GCACTCGCCCGAGGGTTCCGGGA'),
        {2: []}),
        (search.find_by_patterns({2: [r'[TUAGC]{1}[G]', r'[TUAGC]{2}[G]'], 3: [r'[G]{2}', r'[G]{3}']}, 'GCACTCGCCGCGAGGGTTCCTTTA'),
        {2: ['CG', 'TCG', 'CCG', 'GCG', 'GAG', 'AG', 'AGG', 'GG', 'GGG'], 3: ['GG', 'GGG']}),      
        ]
        for test in tests:
            test[0].items().sort()
            test[1].items().sort()
            for k, v in test[0].items():
                v.sort()
            for k, v in test[1].items():
                v.sort()
        
        for actual, expected in tests:
            self.failUnlessEqual(actual, expected)
            
    def test_find_regular2(self):
        """Tests for finding regular expressions without importance number"""
        tests=[
        (search.findall_overlapping(r'[A][G][TUAGC]{5}', 'GCACTCGCCGCGAGGGTTGCCGGGACGGGCCCAAGATGGCTGGGAGCTTTGGTTCCGCTTCGGTCTACCTCGTAGAGCCCCATTCATTACCTTGC'),
        ['AGGGTTG', 'AGATGGC', 'AGCTTTG', 'AGAGCCC', 'AGCCCCA']),
        (search.findall_overlapping(r'[A][TUAGC]{5}[G]', 'GCACTCGCCGCGAGGGTTCCGGGA'),
        [])
        ]
        for test in tests:
            test[1].sort()
            test[0].sort()
        for actual, expected in tests:
            self.failUnlessEqual(actual, expected)   
            
#    def test_find_immuno(self):
#        """Tests for finding immunostimulatory sequences"""
#        tests=[
#        ('UGUGUCTCGCCGCGAGG', ['UGUGU', 'GU']),
#        ('UUUUUGUGUCTCGCCGCGAGG', ['UGUGU', 'GU', 'UUUUU']),
#        ('GTTGCCGGGACGGGCCCGUCCUUCAAAUGGCGTTGCCGGGACGGGCCC', ['GUCCUUCAA', 'GU', 'AU', 'UGGC']),
#        ('GTTGCCGGGACGGGCCC', []),
#        ('', [])
#        ]
#        for test in tests:
#            test[1].sort()
#        for sequence, expected in tests:
#            self.failUnlessEqual(search.find_immuno(sequence).sort(), expected)
            
if __name__ == '__main__':
    unittest.main()