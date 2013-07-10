#!/usr/bin/env python
import re
import math

def check_complementary(seq1,seq2):
    
    def check(seq1,seq2):
        seq1,seq2 = seq1.lower(), seq2.lower()
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
                count+=1
        proc = (count/mini)*100
        return math.floor(proc) 
    
    nr_offset = 3 # number of offset
    for i in range(1,nr_offset):
    
        max1,max2 = max(len(seq1[:-i]),len(seq2)),max(len(seq1),len(seq2[:-i]))
        min1,min2 = min(len(seq1[:-i]),len(seq2)),min(len(seq1),len(seq2[:-i]))

        if (check(seq1[i:], seq2) or check(seq1, seq2[i:])) >= 80:
            #'or' because we need only one 2-sequence which are complementary 
            return (seq1, seq2, 1, "complementary1") #last string for me 

        elif (check(seq1[:-i], seq2[(max1-min1):]) or \
              check(seq1[(max2-min2):],seq2[:-i])) >= 80: 
            return (seq1,seq2,1,"complementary2")

    return (seq1,seq2,2,"non-complementary") 
 

def check_input(seq_to_be_check):
    pattern = re.compile(r'^[acgtACGT]{17,27}$') 
    error = 'insert only one siRNA sequence or both strands of one siRNA at a\
             time; check if both stands are in 5-3 orientation'
    changed = "changed 'u' to 't'"
    correct = "correct sequence"
    
    def check(seq):
        seq = seq.lower() 
        
        if len(seq) > 27 or len(seq) < 17 :
            message = [seq, "to long or to short"], False 

        elif seq[-2:] == 'uu' or seq[-2:] == "tt":
            seq = seq[:-2]
            message = [seq, "cut 'uu' or 'tt'"], True 

        elif pattern.search(seq):
            message = [seq, correct], True 

        elif not pattern(seq):
            message = [seq, "insert only acgtu letters"], False  

    sequence = seq_to_be_check.split(" ") 

    if len(sequence) == 1:
        return check(sequence[0])[0]

    elif len(sequence) == 2:
        ch_seq1,ch_seq2 = check(sequence[0]), check(sequence[1])
        
        if (ch_seq1[1],ch_seq2[1] is True, True) and \
            check_complementary(sequence[0], sequence[1])[2] == 1:
            return [sequence[0], sequence[1], correct]

        else:
            return [ch_seq1[0], ch_seq2[0], "Not complementary"]



#print check_input("acggctTggaacttctggtac")

str1 = 'acggcttGGaacttctggtac' 
str2 = 'gtaccagaagttccaagcc'

str11='acggcttGGaacttctggtac'
str22='gtaccagaagttccaagccgt'

check_complementary(str11,str22)

