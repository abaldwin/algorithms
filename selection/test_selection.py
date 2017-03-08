#!/usr/bin/env python3

import unittest
from random import sample, shuffle
from selection import rselect


class TestSelection(unittest.TestCase):
    def test_selction(self):
        len_input = 10
        input = list(range(0, len_input))
        random_input = list(input)
        shuffle(random_input)
        for ith_order_stat in sample(range(1, 10), 5):
            result = rselect(random_input, ith_order_stat)
            self.assertEqual(result, input[ith_order_stat - 1])


if __name__ == '__main__':
    unittest.main()
