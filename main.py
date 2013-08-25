#!/usr/bin/env python
from utils import check_input
from utils import get_frames
from utils import reverse_complement
import sys

def main(input_str):
	try:
		sequences = check_input(input_str)
	except: #your exception
		return {'errors': "Rivineks errors"}
	for seq1, seq2, shift_left, shift_right in sequences:
		if not seq2:
			seq2 = reverse_complement(seq1)
		frames = get_frames(seq1, seq2, shift_left, shift_right)
		if 'error' in frames: #database error handler
			return frames

if __name__ == '__main__':
	print(main(" ".join(sys.argv[1:])))