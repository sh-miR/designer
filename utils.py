#!/usr/bin/python
import re
import math


string_to_be_check = raw_input("Add sequence: ")


def check_complementary(str1,str2):
    
    def check(str1,str2):
        tran = { "a":"t", "t":"a", "u":"a", "c":"g", "g":"c"}
        str2 = str2[::-1]
        if len(str1)>len(str2):
            mini = float(len(str2))
            maks = float(len(str1))
        else:
            mini = float(len(str1))
            maks = float(len(str2))
        i = 0
        count = 0 
        while i < mini: 
            if tran[str1[i]] == str2[i]:
                count+=1
            i+=1 
        proc = (count/maks)*100
        return math.floor(proc) 
    
    if check(str1,str2) >= 80:
        return (str1,str2,1)
    
    elif check(str1[1:],str2) >= 80:
        return (str1[1:],str2,1,"str[1:]")
    
    elif check(str1[2:],str2) >= 80:
        return (str1[2:],str2,1,"str1[2:]")

    elif check(str1,str2[1:]) >= 80:
        return (str1,str2[1:],1,"str2[1:]")

    elif check(str1,str2[2:]) >= 80:
        return (str1,str2[2:],1,"str2[2:]")
    
    else:
        return (str1,str2,2)


def inputt(string_to_be_check):
    __pattern1 = re.compile(
        r'^[acgtACGT]{17,27}$')
    __pattern2 = re.compile(
        r'^[acgtuACGTU]{17,27}$')
    __pattern3 = re.compile(
        r'^[acgtuACGTU]$' )
    error = 'insert only one siRNA sequence or both strands of one siRNA at a time; check if both stands are in 5-3 orientation'
    changed = "changed 'u' to 't'"

    def check(seq):
        seq = seq.lower() 
    
        if len(seq) > 27 and __pattern3.search(seq) or len(seq) < 17 and __pattern3.search(seq):
            message = [seq, "to long or to short"] 
        
        elif seq[-2:] == 'uu' or seq[-2:] == "tt":
            seq = seq[:-2]
            message = [seq,"cut 'uu' or 'tt'"]

        elif __pattern1.search(seq):
            message = [seq,"correct sequence"] 

        elif __pattern2.search(seq):
            new_string = ""
            for i in seq:
                if i is 'u':
                    new_string+='t'
                else:
                    new_string+=i
            seq = new_string
            message = [seq,changed]

        else:
            message = [seq,"insert only acgtu letters"]
        return message

    sequence = string_to_be_check.split(" ")
    print sequence

#dodac pare ifow i okej
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

print inputt(string_to_be_check)
