#!/usr/bin/env python3

import unittest
from closest_pair import closest_pair, brute_force_closest_pair

class TestClosestPair(unittest.TestCase):
    def test_brute_force_closest_pair(self):
        closest_pairs = [(1, 1), (1, 2)]
        points = closest_pairs + [(3, 0), (4, 9)]
        result = brute_force_closest_pair(points)
        self.assertEqual(result, tuple(closest_pairs))

    def test_closest_pair(self):
        closest_pairs = [(1, 1), (1, 2)]
        points = closest_pairs + [(3, 0), (4, 9)]
        result = closest_pair(points)
        self.assertEqual(result, tuple(closest_pairs))


if __name__ == '__main__':
    unittest.main()