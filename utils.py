#!/usr/bin/env python
import re
import math
import string
from backbone import qbackbone
from backbone import Backbone

def check_complementary_single(seq1, seq2):
        seq1, seq2 = seq1.lower(), seq2.lower()
        tran = { "a":"t", 
                 "t":"a", 
                 "u":"a", 
                 "c":"g", 
                 "g":"c"}
        seq2 = seq2[::-1]
        mini = float(min(len(seq1), len(seq2)))
        count = 0
        for mol1, mol2 in zip(seq1, seq2):
            if tran[mol1] == mol2:
                count += 1
        proc = (count/mini)*100
        return math.floor(proc) 


def check_complementary(seq1, seq2):
        """test for complementary, if both strands are in 5'-3' orientation
class perform only when there are two strands given; should take as input both strand,
input:
5'acggcttGGaactuctggtac3'
5'gtaccagaagttccaagccgt3'
reverse second:
3'tgccgaaccttgaagaccatg5'
translate second strand in a way (a->t, t->a, u->a, c->g, g->c),
5'acggcttGGaactuctggtac3'
check if the strands are the same, starting with first nucleotide or -2,-1,+1,+2 (from the beggining or the end) with minimum 80% similarity

3) 5'acggcttGGaactuctggtac3'
     |||||||||||||||||||||
   3'tgccgaaccttgaagaccatg5'
   5'acggcttGGaactuctggtac3'

output: 'first sequence' (19-21nt), 'second sequence' (19-21nt), left_end{-4,-3,-2,-1,0,1,2,3,4}, rigth_end{-4,-3,-2,-1,0,1,2,3,4}
"""
    
    nr_offset = 3 
    
    if check_complementary_single(seq1, seq2) >= 80:
        return seq1, seq2, 0, 1 

    elif check_complementary_single(seq1[::-1], seq2[::-1]) >= 80:
        return seq1[::-1], seq2[::-1], 0, 2  #<- Return reversed or normal?

    for i in range(1, nr_offset):
        
        max1, max2 = max(len(seq1[:-i]),len(seq2)),max(len(seq1),len(seq2[:-i]))
        min1, min2 = min(len(seq1[:-i]),len(seq2)),min(len(seq1),len(seq2[:-i]))
 
        if check_complementary_single(seq1[i:], seq2) >= 80:
            return seq1[i:], seq2, i, 1 

        elif check_complementary_single(seq1, seq2[i:]) >= 80:
            return seq1, seq2[i:], -i, 1 

        elif check_complementary_single(seq1[:-i], seq2[(max1-min1):]) >= 80: 
            return seq1[:-i], seq2[(max1-min1):], i, 2

        elif check_complementary_single(seq1[(max2-min2):], seq2[:-i]) >= 80:
            return seq1[(max2-min2):], seq2[:-1], -i, 2 

    else:
        return seq1, seq2, 'insert only one siRNA sequence or both strands of \
one siRNA at a time; check if both stands are in 5-3 orientation'


def check_input_single(seq):
    """Function for check sequence from input"""
    seq = seq.lower() 
    seq = seq.replace('u','t') 
    pattern = re.compile(r'^[acgt]{17,27}$') 
    error = 'insert only one siRNA sequence or both strands of one \
siRNA at a time; check if both stands are in 5-3 orientation'


    if len(seq) > 27 or len(seq) < 17:
        return  [seq, "to long or to short", False]

    elif seq[-2:] == "tt" and pattern.search(seq):
        seq = seq[:-2]
        return [seq, "cut 'uu' or 'tt'", True]

    elif pattern.search(seq):
        return [seq, "correct sequence", True] 

    elif not pattern.search(seq):
        return [seq, "insert only acgtu letters", False]

def check_input(seq_to_be_check):
    """Function for checking many sequences and throw error if wrong input
input limitations: possible letters: {ACTGUactgu}, change all 'u' to 't', length 19-21, one strand or two strands splitted by space,
if two strands check if they are in correct 5'-3' orientation, allow |_20%_| mismatches,
if the sequence is correct input returns 'first sequence' (19-21nt), 'second sequence' (19-21nt), left_end{-4,-3,-2,-1,0,1,2,3,4}, rigth_end{-4,-3,-2,-1,0,1,2,3,4}
messages (moga byc potem zmienione numerycznie i komunikaty w programie):
"correct sequence"
"changed 'u' to 't'"
"cut 'uu' or 'tt' ends"
errors:
"too short"
"insert your siRNA sequence"
"too long"
"insert only one siRNA sequence or both strands of one siRNA at a time; check if both stands are in 5'-3' orientation"
"sequence can contain only {actgu} letters""""

    correct = "correct sequence" 
    sequence = seq_to_be_check.split(" ") 
    error = 'insert only one siRNA sequence or both strands of one siRNA at a\
time; check if both stands are in 5-3 orientation'
    
    if len(sequence) == 1:
        return check_input(sequence[0])[:2]

    elif len(sequence) == 2:
        ch_seq1, ch_seq2 = check_input_single(sequence[0]), check_input_single(sequence[1])
        
        if (ch_seq1[1], ch_seq2[1] is True, True) and \
            check_complementary(sequence[0], sequence[1])[2] == 1:
            return [sequence[0], sequence[1], correct]

    else:
        return error 

def complement(sequence):
    """Generates complement sequence to given"""
    return sequence.translate(string.maketrans("ATCG", "TAGC"))

def get_frames(input_seq):
    """Function connecting with backbone database and retruning template"""
    """Take output of check_input function and insert into flanking sequences.
    take from database all miRNA results and check if ends of input is suitable for flanking sequences.
    If first value == and miRNA_end_5 second value == miRNA_end_3 then simply concatenate
    sequences flanks5_s + first_sequence + loop_s + second_sequence + flanks3_s.
    If any end is different function has to modify end of the insert:
    Right end:
    if miRNA_end_5<first_end
    add to right site of second sequence additional nucleotides (as many as |miRNA_end_5 - first_end|)
    like (dots are nucleotides to add, big letter are flanking sequences, small are input):
    AAAGGGGCTTTTagtcttaga
    TTTCCCCGAA....agaatct
    if miRNA_end_5>first_end
    cut nucleotides from rigth site of flanks3_s and/or from right site of second sequence
    before cut:
    AAAGGGGCTTTTagtcttaga
    TTTCCCCGAATTTTcctcagaatct
    after cut:
    AAAGGGGCTTTTagtcttaga
    TTTCCCCGAAAAtcagaatct
    """
   
    
    data = qbackbone('get_all')
    if 'error' in data:
        return data
    try:
        seq1, seq2, shift, end = check_input(input_seq)
    except ValueError:
        error = check_input(input_seq)
        return {'error': error}
    frames = []
    min_len = len(seq1)
    max_len = len(seq2)
    if shift == 0:
        for elem in data:
            frame = Backbone(**elem)
            if frame.miRNA_min <= min_len <= frame.miRNA_max:
                frames.append((frame, seq1, seq2))
    return frames
