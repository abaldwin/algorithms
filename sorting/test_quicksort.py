#!/usr/bin/env python3

import unittest
from random import shuffle
from quicksort import quicksort


class TestQuickSort(unittest.TestCase):

    def test_quicksort(self):
        expected_result = list(range(0, 100))
        unsorted_list = list(expected_result)
        shuffle(unsorted_list)
        result = quicksort(unsorted_list)
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()