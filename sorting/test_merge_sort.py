import unittest
from random import shuffle
from merge_sort import merge_sort_with_heap, merge_sort


class TestMergeSort(unittest.TestCase):

    def test_merge_sort(self):
        expected_output = list(range(0, 1000))
        randomized_input = list(expected_output)
        shuffle(randomized_input)
        result = merge_sort(randomized_input)
        self.assertListEqual(result, expected_output)

    def test_merge_sort_with_heap(self):
        expected_output = list(range(0, 1000))
        randomized_input = list(expected_output)
        shuffle(randomized_input)
        result = merge_sort_with_heap(randomized_input)
        self.assertListEqual(result, expected_output)


if __name__ == '__main__':
    unittest.main()
