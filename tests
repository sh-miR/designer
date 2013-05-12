#!/usr/bin/python
#

"""
Test for shmiR application
"""

import unittest

from shmiR import shmiR

class ShmiRTest(unittest.TestCase):
    def setUp(self):
        """data"""
        self.prog = shmiR()
   
    def test_input(self):
        """test for input
        input limitations: possible letters: {ACTGUactgu}, change all 'u' to 't', length 17-27, one strand or two strands splitted by space,
        if two strands check if they are in correct 5'-3' orientation, allow |_20%_| mismatches, only two additional end nucleotides,
        for sequences with last (3') two 'tt' or'uu' and length >=21 cut those ends
        if the sequence is correct input returns ('sequence', 'message'), otherwise only 'error'
        messages (moga byc potem zmienione numerycznie i komunikaty w programie):
        "correct sequence"
        "changed 'u' to 't'"
        "cut 'uu' or 'tt' ends"
        errors:
        "too short"
        "insert your siRNA sequence"
        "too long"
        "insert only one siRNA sequence or both strands of one siRNA at a time; check if both stands are in 3'-5' orientation"
        "sequence can contain only {actgu} letters"

        5'acggcttGGaactuctggtac3'
          |||||||||||||||||||||
        3'tgccgaaccttgaagaccatg5'
        5'gtaccagaagttccaagccgt3'
        """


        tests = [
            ('acggctTggaacttctggtac', ('acggcttggaactuctggtac', 'correct sequence')),
            ('acggcttGGaacttctggtac gtaccagaagttccaagccgt', ('acggcttGGaacttctggtac gtaccagaagttccaagccgt', 'correct sequence')),
            ('acggcttggAActuctggtac gtaccagaagttccaagccgt', ('acggcttGGaacttctggtac gtaccagaagttccaagccgt', 'changed u to t')),
            ('acggctTggaacttctggtacTT', ('acggctTggaacttctggtac', 'cut uu or tt ends')),
            ('acggcttggaactuct', 'too short'),
            ('', 'insert your siRNA sequence'),
            ('acttctggtacTTUUUUUUuuuuuuGGG', 'too long'),
            ('acggcttGGaacttctggtac gtaccagaagttccaagccgt acggcttGGaacttctggtac', 'insert only one siRNA sequence or both strands of one siRNA at a time; check if both stands are in 5-3 orientation'),
            ('acggcttGGaacttctggtac tgccgaaccttgaagaccatg', 'insert only one siRNA sequence or both strands of one siRNA at a time; check if both stands are in 5-3 orientation'),
            ('acggctTggaacttctggtwacTT', 'sequence can contain only {actgu} letters')
            ]
        for list1, expected in tests:
            self.failUnlessEqual(self.prog.input(list1), expected)



    
    def test_check_complementary(self):
        """test for complementary, if both strands are in 5'-3' orientation
        class perform only when there are two strands given; should take as input both strand,
        reverse second strand,
        translate reversed strand in a way (a->t, t->a, u->a, c->g, g->c),
        check if the strands are the same, starting with first nucleotide or -2,-1,+1,+2 with minimum 80% similarity
        (last thing can be performed with blast)

           5'acggcttGGaactuctggtac3'
             |||||||||||||||||||||
           3'tgccgaaccttgaagaccatg5'
        1) 5'gtaccagaagttccaagccgt3'
        2) 5'acggcttGGaactuctggtac3'
        3) 5'acggcttGGaactuctggtac3'
             |||||||||||||||||||||
           5'acggcttGGaactuctggtac3'
        output: 1 - complementary
                2 - noncomplementary
                3 - incorrect input
        """


        tests = [

            ('acggctTggaacttctggtac', 3),
            ('acggcttGGaacttctggtac gtaccagaagttccaagccgt', 1),
            ('acggcttGGaacttctggtac gtaccagaagttccaagccgta', 1),
            ('acggcttGGaacttctggtac gtaccagaagttccaagcc', 1),
            ('acggcttGGaacttctggtac gaaggtgaagttccaagccgt', 1),
            ('acggcttGGaacttctggtac gaaggtgaagccccaagccgt', 2), #>20% mismaches
            ('acggcttGGaacttctggtac gtaccagaagttccaagccgttua', 2), #+3
            ('acggcttggAActuctggtac acggcttggAActuctggtac', 2), #both same strands
            ('acggcttggAActuctggtac acggcttggAActuctggtac gtaccagaagttccaagccgt', 3)
            ]
        for list1, expected in tests:
            self.failUnlessEqual(self.prog.complementary(list1), expected)

if __name__ == '__main__':
    unittest.main()
