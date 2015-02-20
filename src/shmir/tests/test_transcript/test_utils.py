import unittest

from shmir.designer.transcript.utils import (
    create_path_string,
    merge_results,
    unpack_dict_to_list
)


class TestUtils(unittest.TestCase):

    def test_unpack_dict_to_list(self):
        result = unpack_dict_to_list({'a': ['b', 'c'], 'd': ['e', 'f']})
        self.assertEqual(
            list(result),
            [('a', 'b'), ('d', 'e'), ('a', 'c'), ('d', 'f')]
        )

    def test_create_path_string(self):
        result = create_path_string('a', 'b', 'c')
        self.assertEqual(result, 'a_b_c')

    def test_merge_results(self):
        result = merge_results([{'a': 'b'}])
        self.assertEqual(result['a'], ['b'])
