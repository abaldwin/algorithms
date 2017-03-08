#!/usr/bin/env python3

import collections
import unittest
from two_sum import two_sum, two_sum2


class TestTwoSum(unittest.TestCase):
    def test_two_sum(self):
        input = [10000, 2, 1, 9999, 2]
        result = two_sum(input)
        self.assertEqual(result, 2)


if __name__ == '__main__':
    unittest.main()