#!/usr/bin/env python
from utils import check_input
from utils import get_frames
from utils import reverse_complement
from utils import score_homogeneity
from utils import two_same_strands_score
from backbone import get_by_name
import sys

def main(input_str):
    sequence = check_input(input_str)
    seq1, seq2, shift_left, shift_right = sequence
    if not seq2:
        seq2 = reverse_complement(seq1)
    frames = get_frames(seq1, seq2, shift_left, shift_right)
    if 'error' in frames: #database error handler
        return frames

    orginal_frames = [get_by_name(structure.name) for structure in frames]
    
    frames_with_score = []
    for frame, orginal in zip(frames, orginal_frames):
        score = 0
        #TODO SSFROM FRAME - MFOLD
        score += score_frame(frame, SSFROMFRAME, orginal)
        score += score_homogeneity(orignal) #change interface in utils
        score += two_same_strands_score(seq1, orginal) #change interface
        frames_with_score.append((score, frame))

    return frames_with_score


if __name__ == '__main__':
    print(main(" ".join(sys.argv[1:])))