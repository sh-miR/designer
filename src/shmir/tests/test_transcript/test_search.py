import unittest

from shmir.designer.transcript.search import (
    all_possible_sequences,
    findall_overlapping,
    find_by_patterns,
)


class TestSearch(unittest.TestCase):

    def test_findall_overlapping(self):
        result = findall_overlapping('[abcd]+', 'abcd')
        self.assertEqual(result, set(['abcd', 'bcd', 'cd', 'd']))

    def test_find_by_patterns(self):
        patterns = {3: 'a', 2: 'bc'}
        result = find_by_patterns(patterns, 'abcd')

        self.assertEqual(list(result[3]), list(patterns[3]))
        self.assertEqual(list(result[2]), list(patterns[2]))

    def test_all_possible_sequences(self):
        all_sequences = all_possible_sequences('acgt', 1, max_len=4)
        self.assertEqual(
            list(all_sequences),
            ['a', 'ac', 'acg', 'acgt', 'c', 'cg', 'cgt', 'g', 'gt', 't']
        )
