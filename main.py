#!/usr/bin/env python
from utils import check_input
from utils import get_frames
from utils import reverse_complement
import sys

def main(input_str):
    sequence = check_input(input_str)
    seq1, seq2, shift_left, shift_right = sequence
    if not seq2:
        seq2 = reverse_complement(seq1)
    frames = get_frames(seq1, seq2, shift_left, shift_right)
    if 'error' in frames: #database error handler
        return frames

    for frame in frames:
        score = 0
        


if __name__ == '__main__':
    print(main(" ".join(sys.argv[1:])))