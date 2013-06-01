#!/usr/bin/python
import re
import math


seq_to_be_check = raw_input("Add sequence: ")


def check_complementary(seq1,seq2):
    
    def check(seq1,seq2):
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

    def check(seq):
        seq = seq.lower() 
        if len(seq) > 27 or len(seq) < 17 :
            message = [seq, "to long or to short"] 
        
        elif seq[-2:] == 'uu' or seq[-2:] == "tt":
            seq = seq[:-2]
            message = [seq,"cut 'uu' or 'tt'"]

        elif __pattern.search(seq):
            message = [seq,"correct sequence"] 

        elif 'u' in seq:
            seq = seq.replace('u','t')
            message = [seq,changed] 

        else:
            message = [seq,"insert only acgtu letters"]
        return message

    sequence = seq_to_be_check.split(" ")
    print sequence

#do naprawy to na dole w (niedziele) 
    if len(sequence) == 2:
        zm = [check(sequence[0]),check(sequence[1])]
        print zm
        if (zm[0][1] == zm[1][1] == "correct sequence") and (check_complementary(zm[0][0],zm[1][0])[2] == 1) :
            return [zm[0][0],zm[1][0],"correct sequence"]
        
        elif (zm[0][1] == error or zm[1][1] == error) or ((zm[0][1] == zm[1][1] == "correct sequence") and (check_complementary(zm[0][0],zm[1][0])[2] == 2)):
                return [zm[0][0],zm[1][0],error]

        elif ( zm[0][1] == changed  or zm[1][1] == changed ) and (check_complementary(zm[0][0],zm[1][0])[2] == 1):
            return [zm[0][0],zm[1][0],changed]


    elif len(sequence) == 1:
        return check(sequence[0])
    else:
        return error    
        
    
    

cos = check_complementary("tact","tga")

print check_input(seq_to_be_check)
