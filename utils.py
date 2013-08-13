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
    """Checking complementary function""" 
    
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
    """Function for checking many sequences and throw error if wrong input"""

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

def reverse_complement(sequence):
    """Generates reverse complement sequence to given"""
    return sequence.translate(string.maketrans("ATCG", "TAGC"))[::-1]

def get_frames(seq1, seq2, shift_left, shift_right):
    """Function connecting with backbone database and retruning template"""
    data = qbackbone('get_all')
    if 'error' in data:
        return data
    frames = []
    min_len = len(seq1)
    max_len = len(seq2)
    if shift_left == 0 and shift_right == 0:
        for elem in data:
            frame = Backbone(**elem)
            if frame.miRNA_min <= min_len <= frame.miRNA_max:
                frames.append((frame, seq1, seq2))
    return frames

