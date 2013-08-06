#!/usr/bin/python
#

"""
Test for shmiR application
"""

import unittest
import utils

class ShmiRTest(unittest.TestCase):
    
    #def test_input(self):
    """test for input
input limitations: possible letters: {ACTGUactgu}, change all 'u' to 't', length 17-27, one strand or two strands splitted by space,
if two strands check if they are in correct 5'-3' orientation, allow |_20%_| mismatches, only two additional end nucleotides,
for sequences with last (3') two 'tt' or'uu' cut those ends
if the sequence is correct input returns ('sequence'), otherwise only 'error'
messages (moga byc potem zmienione numerycznie i komunikaty w programie):
"correct sequence"
"changed 'u' to 't'"
"cut 'uu' or 'tt' ends"
errors:
"too short"
"insert your siRNA sequence"
"too long"
"insert only one siRNA sequence or both strands of one siRNA at a time; check if both stands are in 5'-3' orientation"
"sequence can contain only {actgu} letters"

5'acggcttGGaactuctggtac3'
  |||||||||||||||||||||
3'tgccgaaccttgaagaccatg5'
5'gtaccagaagttccaagccgt3'
"""


        #tests = [
            #('acggctTggaacttctggtac', ['acggcttggaacttctggtac', 'correct sequence']),
            #('acggcttGGaacttctggtac gtaccagaagttccaagccgt', ['acggcttggaacttctggtac', 'gtaccagaagttccaagccgt', 'correct sequence']),
            #('acggcttggAActuctggtac gtaccagaagttccaagccgt', ['acggcttggaacttctggtac', 'gtaccagaagttccaagccgt', "changed 'u' to 't'"]),
           # ('acggctTggaacttctggtacTT', ['acggcttggaacttctggtac', "cut 'uu' or 'tt'"]),
            #('acggcttggaactuct',"to long or to short"),
            #('', "to long or to short"),
            #('acttctggtacTTUUUUUUuuuuuuGGG', "to long or to short"),
            #('acggcttGGaacttctggtac gtaccagaagttccaagccgt acggcttGGaacttctggtac', 'insert only one siRNA sequence or both strands of one siRNA at a time; check if both stands are in 5-3 orientation'),
            #('acggcttGGaacttctggtac tgccgaaccttgaagaccatg', 'insert only one siRNA sequence or both strands of one siRNA at a time; check if both stands are in 5-3 orientation'),
            #('acggctTggaacttctggtwacTT', 'sequence can contain only {actgu} letters')
      #      ]
      #  for list1, expected in tests:
      #      self.failUnlessEqual(utils.check_input(list1), expected) 


    
    def test_check_complementary(self):
        """test for complementary, if both strands are in 5'-3' orientation
class perform only when there are two strands given; should take as input both strand,
input:
5'acggcttGGaactuctggtac3'
5'gtaccagaagttccaagccgt3'
reverse second:
3'tgccgaaccttgaagaccatg5'
translate second strand in a way (a->t, t->a, u->a, c->g, g->c),
5'acggcttGGaactuctggtac3'
check if the strands are the same, starting with first nucleotide or -2,-1,+1,+2 with minimum 80% similarity
(last thing can be performed with blast)

3) 5'acggcttGGaactuctggtac3'
     |||||||||||||||||||||
   3'tgccgaaccttgaagaccatg5'
   5'acggcttGGaactuctggtac3'

output: 1 - complementary
2 - noncomplementary
"""


        tests = [
            ('acggcttGGaacttctggtac', 'gtaccagaagttccaagccgt', ('acggcttGGaacttctggtac', 'gtaccagaagttccaagccgt', 0, 1)),
            ('acggcttGGaacttctggtac', 'cgtaccagaagttccaagccgt', ('acggcttGGaacttctggtac', 'cgtaccagaagttccaagccgt', 0, 1)),
            #('acggcttGGaacttctggtac', 'gtaccagaagttccaagcc', ('acggcttGGaacttctggtac', 'gtaccagaagttccaagcc', -2,  1)),
            ('acggcttGGaacttctggtac', 'gaaggtgaagttccaagccgt', ('acggcttGGaacttctggtac', 'gaaggtgaagttccaagccgt', 0, 1)),
            #('acggcttGGaacttctggtac', 'gaaggtgaagccccaagccgt', ('acggcttGGaacttctggtac', 'gaaggtgaagccccaagccgt', 2)), #>20% mismaches
            #('acggcttGGaacttctggtac', 'gtaccagaagttccaagccgttua', ('acggcttGGaacttctggtac', 'gtaccagaagttccaagccgttua', 0, 2)), #+3
            #('acggcttggAActuctggtac', 'acggcttggAActuctggtac', ('acggcttggAActuctggtac', 'acggcttggAActuctggtac', 2)), #both same strands
            #('acggcttGGaacttctggtac', 'gtaccagaagttccaagccgta', ('acggcttGGaacttctggtac', 'gtaccagaagttccaagccgta', 1, 1)),
            ('acggcttGGaacttctggtac', 'gtaccagaagttccaagccgtag', ('acggcttGGaacttctggtac', 'gtaccagaagttccaagccgt', -2,1)),
            ('acggcttGGaacttctggtac', 'gtaccagaagttccaagccgta', ('acggcttGGaacttctggtac', 'gtaccagaagttccaagccgt', -1,1)),
            ('acggcttGGaacttctggtac', 'gtaccagaagttccaagccgt', ('acggcttGGaacttctggtac', 'gtaccagaagttccaagccgt', 0,1)),
            ('acggcttGGaacttctggtac', 'gtaccagaagttccaagccg', ('acggcttGGaacttctggtac', 'gtaccagaagttccaagccg', 1,1)),
            ('acggcttGGaacttctggtac', 'gtaccagaagttccaagcc', ('acggcttGGaacttctggtac', 'gtaccagaagttccaagcc', 2,1)),
            ('acggcttGGaacttctggtac', 'gagtaccagaagttccaagccgt', ('acggcttGGaacttctggtac', 'gtaccagaagttccaagccgt',-2,2)),
            ('acggcttGGaacttctggtac', 'agtaccagaagttccaagccgt', ('acggcttGGaacttctggtac', 'gtaccagaagttccaagccgt', -1,2)),
            ('acggcttGGaacttctggtac', 'gtaccagaagttccaagccgt', ('acggcttGGaacttctggtac', 'gtaccagaagttccaagccgt', 0,2)),
            ('acggcttGGaacttctggtac', 'taccagaagttccaagccgt', ('acggcttGGaacttctggta', 'taccagaagttccaagccgt', 1,2)),
            ('acggcttGGaacttctggtac', 'accagaagttccaagccgt', ('acggcttGGaacttctggt', 'accagaagttccaagccgt', 2,2))
            ]
        for seq1, seq2, expected in tests:
            self.failUnlessEqual(utils.check_complementary(seq1, seq2), expected)

    #def test_get_frames(self):

     #   tests = [
     #       ('', ()),
     #       ('', ())
     #       ]
     #   for sequences, expected in tests:
     #       self.failUnlessEqual(utils.get_frames(sequences), expected)


if __name__ == '__main__':
    unittest.main()
