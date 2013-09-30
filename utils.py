import re
import math
import string

from backbone import get_all
from backbone import get_by_name
from backbone import Backbone
from backbone import get_by_name
from ss import parse
from ss import parse_score

import errors
import logging


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
    class perform only when there are two strands given; should take as input
    both strand,
    input:
    5'acggcttGGaactuctggtac3'
    5'gtaccagaagttccaagccgt3'
    reverse second:
    3'tgccgaaccttgaagaccatg5'
    translate second strand in a way (a->t, t->a, u->a, c->g, g->c),
    5'acggcttGGaactuctggtac3'
    check if the strands are the same,
    starting with first nucleotide or -2,-1,
    +1,+2 (from the beggining or the end) with minimum 80% similarity

    3) 5'acggcttGGaactuctggtac3'
         |||||||||||||||||||||
       3'tgccgaaccttgaagaccatg5'
       5'acggcttGGaactuctggtac3'

    output: 'first sequence' (19-21nt), 'second sequence' (19-21nt), left_end
    {-4,-3,-2,-1,0,1,2,3,4}, rigth_end{-4,-3,-2,-1,0,1,2,3,4}
    """
    nr_offset = 5
    tab = []
    end_offset = len(seq1)-len(seq2)
    if check_complementary_single(seq1, seq2) >= 80:
        tab.append((seq1, seq2, 0, end_offset))

    for offset in range(1, nr_offset):
        if check_complementary_single(seq1[offset:], seq2) >= 80:
            end_offset = len(seq1)-len(seq2)-offset
            tab.append((seq1, seq2, offset, end_offset))
        if check_complementary_single(seq1, seq2[:-offset]) >= 80:
            end_offset = len(seq1)-len(seq2)+offset
            tab.append((seq1, seq2, -offset, end_offset))
    if not tab:
        raise errors.InputException(errors.error)
    return tab[0]


def check_input_single(seq):
    """Function for check sequence from input"""
    seq = seq.lower().replace('u','t')
    pattern = re.compile(r'^[acgt]{19,21}$')
    cut_warn = "cut 'uu' or 'tt'"

    if not pattern.search(seq):
        if len(seq) > 21 or len(seq) < 19:
            raise errors.InputException('%s' % errors.len_error)
        raise errors.InputException('%s' % errors.patt_error)
    elif seq[-2:] == "tt" and pattern.search(seq):
        seq = seq[:-2]
        logging.warn(cut_warn)
        return [seq, cut_warn, True]
    elif pattern.search(seq):
        return [seq, None, True]


def check_input(seq_to_be_check):
    """Function for checking many sequences and throw error if wrong input
    input limitations: possible letters: {ACTGUactgu}, change all 'u' to 't',
    length 19-21, one strand or two strands splitted by space,
    if two strands check if they are in correct 5'-3' orientation, allow |_20%_|
    mismatches,
    if the sequence is correct input returns 'first sequence' (19-21nt), 'second
    sequence' (19-21nt), left_end{-4,-3,-2,-1,0,1,2,3,4},
    rigth_end{-4,-3,-2,-1,0,1,2,3,4}
    messages (moga byc potem zmienione numerycznie i komunikaty w programie):
    "correct sequence"
    "changed 'u' to 't'"
    "cut 'uu' or 'tt' ends"
    errors:
    "too short"
    "insert your siRNA sequence"
    "too long"
    "insert only one siRNA sequence or both strands of one siRNA at a time;
    check if both stands are in 5'-3' orientation"
    "sequence can contain only {actgu} letters"""
    sequence = seq_to_be_check.split(" ")
    error = 'insert only one siRNA sequence or both strands of one siRNA at a'\
        'time; check if both stands are in 5-3 orientation'
    len_seq = len(sequence)
    if len_seq == 1:
        return check_input_single(sequence[0])[:1]
    elif len_seq != 2:
        raise errors.InputException('%s' % errors.error)
    elif len_seq == 2:
        ch_seq1, ch_seq2 = check_input_single(sequence[0]), \
            check_input_single(sequence[1])
        if (ch_seq1[2], ch_seq2[2] is True, True) :
            return [check_complementary(ch_seq1[0], ch_seq2[0])]


def reverse_complement(sequence):
    """Generates reverse complement sequence to given"""
    return sequence.translate(string.maketrans("ATCG", "TAGC"))[::-1]

def get_frames(seq1, seq2, shift_left, shift_right):
    """Take output of check_input function and insert into flanking sequences.
    take from database all miRNA results and check if ends of input is suitable
    for flanking sequences.
    If first value == and miRNA_end_5 second value == miRNA_end_3 then simply
    concatenate
    sequences flanks5_s + first_sequence + loop_s + second_sequence + flanks3_s.
    If any end is different function has to modify end of the insert:
    Right end:
    if miRNA_end_5<first_end
    add to right site of second sequence additional nucleotides (as many as |
        miRNA_end_5 - first_end|)
    like (dots are nucleotides to add, big letter are flanking sequences, small
        are input):
    AAAGGGGCTTTTagtcttaga
    TTTCCCCGAA....agaatct
    if miRNA_end_5>first_end
    cut nucleotides from rigth site of flanks3_s and/or from right site of
    second sequence
    before cut:
    AAAGGGGCTTTTagtcttaga
    TTTCCCCGAAAATTcctcagaatct (-2, +2)
    After
    AAAGGGGCTTTTagtcttaga
    TTTCCCCGAAAAtcagaatct
    Returns list of tuples (frame, sequence_1 sequence_2)
    """
    data = get_all()
    if error in data:
        return error
    frames = []
    for elem in data:
        frame = Backbone(**elem)
        if shift_left == frame.miRNA_end_5 and shift_right == frame.miRNA_end_5:
            frames.append([frame, seq1, seq2])
        else:
            _seq1 = seq1[:]
            _seq2 = seq2[:]
            #miRNA 5 end (left)
            if frame.miRNA_end_5 < shift_left:
                if frame.miRNA_end_5 < 0 and shift_left < 0:
                    _seq2 += reverse_complement(
                        frame.flanks5_s[frame.miRNA_end_5:shift_left])
                elif frame.miRNA_end_5 < 0 and shift_left > 0:
                    frame.flanks5_s = frame.flanks5_s[:frame.miRNA_end_5]
                    _seq2 += reverse_complement(_seq1[:shift_left])
                elif shift_left == 0:
                    _seq2 += reverse_complement(
                        frame.flanks5_s[:frame.miRNA_end_5])
                elif frame.miRNA_end_5 == 0:
                    _seq2 += reverse_complement(_seq1[:frame.miRNA_end_5])
                else:
                    _seq2 += reverse_complement(
                        _seq1[frame.miRNA_end_5:shift_left])
            elif frame.miRNA_end_5 > shift_left:
                if frame.miRNA_end_5 > 0 and shift_left < 0:
                    frame.flanks5_s += reverse_complement(
                        _seq2[frame.miRNA_end_5:])
                    frame.flanks3_s = frame.flanks3_s[frame.miRNA_end_5:]
                elif frame.miRNA_end_5 > 0 and shift_left > 0:
                    frame.flanks5_s += reverse_complement(
                        frame.flanks3_s[shift_left:frame.miRNA_end_5])
                elif shift_left == 0:
                    frame.flanks5_s += reverse_complement(
                        frame.flanks3_s[:frame.miRNA_end_5])
                elif frame.miRNA_end_5 == 0:
                    frame.flanks5_s += reverse_complement(_seq2[shift_left:])
                else:
                    frame.flanks5_s += reverse_complement(
                        _seq2[shift_left:frame.miRNA_end_5])

            #miRNA 3 end (right)
            if frame.miRNA_end_3 < shift_right:
                if frame.miRNA_end_3 < 0 and shift_right > 0:
                    frame.loop_s = frame.loop_s[-frame.miRNA_end_3:]
                    frame.loop_s += reverse_complement(
                        _seq1[-shift_right:])
                elif frame.miRNA_end_3 > 0 and shift_right > 0:
                    frame.loop_s += reverse_complement(
                        _seq1[-shift_right:-frame.miRNA_end_3])
                elif frame.miRNA_end_3 == 0:
                    frame.loop_s += reverse_complement(_seq1[-shift_right:])
                elif shift_right == 0:
                    frame.loop_s += reverse_complement(
                        frame.loop_s[:-frame.miRNA_end_3])
                else:
                    frame.loop_s += reverse_complement(
                        frame.loop_s[-shift_right:-frame.miRNA_end_3])
            elif frames.miRNA_end_3 > shift_right:
                if frame.miRNA_end_3 > 0 and shift_right < 0:
                    _seq1 += reverse_complement(
                        _seq2[:-shift_right])
                    frame.loop_s = frame.loop_s[:-frame.miRNA_end_3]
                elif frame.miRNA_end_3 > 0 and shift_right > 0:
                    _seq1 += reverse_complement(
                        frame.loop_s[-frame.miRNA_end_3:-shift_right])
                elif shift_right == 0:
                    _seq1 += reverse_complement(
                        frame.loop_s[:frame.miRNA_end_3])
                elif frame.miRNA_end_3 == 0:
                    _seq1 += reverse_complement(_seq2[:-shift_right])
                else:
                    _seq1 += reverse_complement(
                        _seq2[-frame.miRNA_end_3:-shift_right])

            frames.append([frame, _seq1, _seq2])
    return frames


def score_frame(frame, frame_ss_file, orginal_frame):
    """
    frame is a tuple of object Backbone and two sequences
    frame_ss_file is file from mfold
    orignal_frame is object Backbone from database (not changed)
    """
    structure, seq1, seq2 = frame
    structure_ss = parse(frame_ss_file)
    orginal_score = parse_score(orginal_frame.structure)


def score_2():
    #dodaje/odejmuje do obu; w prawej kolumnie tylko gdy jest wieksze od wartosci na ktorej jestesmy zera nie ruszac
    structure = Backbone(**get_by_name('miR-155'))
    orginal_frame = Backbone(**get_by_name('miR-155'))
    seq1, seq2 = 'UUUGUAUUCAGCCCAUAGCGC', 'CGCUAUGGCGAAUACAAACA'
    structure_ss = parse('155LUC_NEW.ss')
    orginal_score = parse_score('structures/miR-155')
    #da differences
    flanks5 = len(orginal_frame.flanks5_s) - len(structure.flanks5_s)
    insertion1 = len(orginal_frame.miRNA_s) - len(seq1)
    loop = len(orginal_frame.loop_s) - len(structure.loop_s)
    insertion2 = len(orginal_frame.miRNA_a) - len(seq2)
    flanks3 = len(orginal_frame.flanks3_s) - len(structure.flanks3_s)
    
    position = len(structure.flanks5_s) #position in sequence (list)
    structure_len = len(structure.template(seq1, seq2))
    current = position + flanks5 #current position (after changes)
    
    if flanks5 < 0:
        add_shifts(0, structure_len, structure_ss, flanks5, 0)
    else:
        add_shifts(position, structure_len,\
                       structure_ss, flanks5, current)
    for diff, nucleotides in [(insertion1, seq1), (loop, structure.loop_s),\
        (insertion2, seq2), (flanks3, '')]:
        position += len(nucleotides)
        current = position + diff
        add_shifts(position, structure_len, structure_ss, diff, current)
    score = 0
    for shmir in structure_ss: 
        for template in orginal_score:
            if shmir == template[0]:
                score += template[1]
    return score, structure_ss


def add_shifts(start, end, frame_ss, value, current):
    for num in range(end):
        if num >= start:
            frame_ss[num][0] += value
        if frame_ss[num][1] != 0 and frame_ss[num][1] > current:
            frame_ss[num][1] += value


def score_homogeneity(struc_name):
    """We are taking value homogenity from database and multiply it 4 times """
    return Backbone(**get_by_name(struc_name)["result"]).homogeneity*3


def two_same_strands_score(seq1, struc_name):
    miRNA_s = Backbone(**get_by_name(struc_name)["result"]).miRNA_s[:2].lower()
    seq = seq1[:2].lower()
    if seq == miRNA_s:
        return 10
    elif seq[0] == miRNA_s[0]:
        return 4
    else:
        return 0

poprawne = [[1, 0], [2, 0], [3, 107], [4, 106], [5, 105], [6, 0], [7, 0], [8, 0], [9, 0], [10, 0], [11, 99], [12, 98], [13, 97], [14, 96], [15, 95], [16, 0], [17, 91], [18, 90], [19, 89], [20, 88], [21, 87], [22, 86], [23, 83], [24, 82], [25, 81], [26, 80], [27, 79], [28, 78], [29, 77], [30, 76], [31, 75], [32, 74], [33, 73], [34, 0], [35, 72], [36, 71], [37, 70], [38, 0], [39, 69], [40, 68], [41, 67], [42, 66], [43, 65], [44, 64], [45, 0], [48, 0], [49, 0], [50, 59], [51, 58], [52, 57], [53, 0], [54, 0], [55, 0], [56, 0], [57, 52], [58, 51], [59, 50], [60, 0], [61, 0], [62, 0], [63, 0], [64, 44], [65, 43], [66, 42], [67, 41], [68, 40], [69, 39], [70, 37], [71, 36], [72, 35], [73, 33], [74, 32], [75, 31], [76, 30], [77, 29], [78, 28], [79, 27], [80, 26], [81, 25], [82, 24], [83, 23], [86, 22], [87, 21], [88, 20], [89, 19], [90, 18], [91, 17], [92, 0], [93, 0], [94, 0], [95, 15], [96, 14], [97, 13], [98, 12], [99, 11], [100, 0], [101, 0], [102, 0], [103, 0], [104, 0], [105, 5], [106, 4], [107, 3], [108, 0], [109, 141], [110, 140], [111, 139], [112, 0], [113, 137], [114, 136], [115, 135], [116, 134], [117, 133], [118, 0], [119, 0], [120, 129], [121, 128], [122, 0], [123, 0], [124, 0], [125, 0], [126, 0], [127, 0], [128, 121], [129, 120], [130, 0], [131, 0], [132, 0], [133, 117], [134, 116], [135, 115], [136, 114], [137, 113], [138, 0], [139, 111], [140, 110], [141, 109], [142, 0], [143, 0], [144, 0], [145, 0], [146, 0], [147, 0], [148, 0], [149, 0], [150, 0], [151, 0], [152, 0]]

def porownywarka():
    bad = []
    ss = score_2()[1]
    for number, elem in enumerate(zip(ss, poprawne)):
        if elem[0] != elem[1]:
            bad.append(number)
    if not bad: #LOL
        print('Wynik poprawny')
    else:
        print("Poprawne | Niepoprawne")
        for elem in bad:
            print "%s | %s" % (poprawne[elem], ss[elem])
    return bad

