#!/usr/bin/python
import re
import math

def check_complementary(seq1,seq2):
    
    def check(seq1,seq2):
        seq1,seq2 = seq1.lower(), seq2.lower()
        tran = { "a":"t", "t":"a", "u":"a", "c":"g", "g":"c"}
        seq2 = seq2[::-1]
        maks = float(max(len(seq1), len(seq2)))
        count = 0
        for mol1, mol2 in zip(seq1, seq2):
            if tran[mol1] == mol2:
                count+=1
        proc = (count/maks)*100
        return math.floor(proc) 
    
    if check(seq1,seq2) >= 80:
        return (seq1,seq2,1)
    
    elif check(seq1[1:],seq2) >= 80:
        return (seq1[1:],seq2,1,"seq[1:]")
    
    elif check(seq1[2:],seq2) >= 80:
        return (seq1[2:],seq2,1,"seq1[2:]")

    elif check(seq1,seq2[1:]) >= 80:
        return (seq1,seq2[1:],1,"seq2[1:]")

    elif check(seq1,seq2[2:]) >= 80:
        return (seq1,seq2[2:],1,"seq2[2:]")
    
    else:
        return (seq1,seq2,2)

def check_input(seq_to_be_check):
    __pattern = re.compile(
        r'^[acgtACGT]{17,27}$') 
    error = 'insert only one siRNA sequence or both strands of one siRNA at a time; check if both stands are in 5-3 orientation'
    changed = "changed 'u' to 't'"
    correct = "correct sequence"
    def check(seq):
        seq = seq.lower() 
               
        if seq[-2:] == 'uu' or seq[-2:] == "tt":
            seq = seq[:-2]
            message = [seq,"cut 'uu' or 'tt'"], True
         
        if len(seq) > 27 or len(seq) < 17 :
            message = [seq, "to long or to short"], False 

        elif __pattern.search(seq):
            message = [seq,correct], True 

        elif 'u' in seq:
            seq = seq.replace('u','t')
            message = [seq,changed],True 

        elif not __pattern(seq):
            message = [seq,"insert only acgtu letters"],False
        else:
            message = [seq,error],False
        return message

    sequence = seq_to_be_check.split(" ") 

    if len(sequence)==1:
        return check(sequence[0])[0]
    elif len(sequence)==2:
        ch_seq1,ch_seq2 = check(sequence[0]), check(sequence[1])
        if (ch_seq1[1],ch_seq2[1] is True,True) and check_complementary(sequence[0],sequence[1])[2]==1:
            return [sequence[0],sequence[1],correct]
        else:
            return [ch_seq1[0],ch_seq2[0],"Not complementary"]



#uncomment to check if its worikng coz tests are little diffrent and I have to w8 for Martyna to approve it <3
#print check_input("acggctTggaacttctggtac")

#print check_input('acggcttGGaacttctggtac gtaccagaagttccaagccgt')
