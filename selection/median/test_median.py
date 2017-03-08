#!/usr/bin/env python3

import unittest
from median import Median


class TestMedian(unittest.TestCase):

    def setUp(self):
        self.heap = Median()

    def test_init(self):
        m = Median()
        self.assertEqual(m._median, 0)
        self.assertIsInstance(m.heap_low, list)
        self.assertIsInstance(m.heap_high, list)
        self.assertListEqual(m.heap_low, [])
        self.assertListEqual(m.heap_high, [])

    def test_push_to_heap_low(self):
        self.heap._push_to_heap_low(5)
        self.assertListEqual(self.heap.heap_low, [5])
        self.heap._push_to_heap_low(20)
        self.assertListEqual(self.heap.heap_low, [20, 5])
        self.heap._push_to_heap_low(7)
        self.assertListEqual(self.heap.heap_low, [20, 5, 7])
        self.assertListEqual(self.heap._heapified_heap_low(), [20, 5, 7])
        self.heap._push_to_heap_low(25)
        self.assertListEqual(self.heap.heap_low, [25, 20, 7, 5])
        self.assertListEqual(self.heap._heapified_heap_low(), [25, 20, 7, 5])
        self.heap._push_to_heap_low(16)
        self.assertListEqual(self.heap.heap_low, [25, 20, 7, 5, 16])
        self.assertListEqual(self.heap._heapified_heap_low(), [25, 20, 7, 5, 16])
        self.heap._push_to_heap_low(14)
        self.assertListEqual(self.heap.heap_low, [25, 20, 14, 5, 16, 7])
        self.assertListEqual(self.heap._heapified_heap_low(), [25, 20, 14, 5, 16, 7])
        self.heap._push_to_heap_low(15)
        self.assertListEqual(self.heap.heap_low, [25, 20, 15, 5, 16, 7, 14])
        self.assertListEqual(self.heap._heapified_heap_low(), [25, 20, 15, 5, 16, 7, 14])
        self.heap._push_to_heap_low(15)
        self.assertListEqual(self.heap.heap_low, [25, 20, 15, 15, 16, 7, 14, 5])
        self.assertListEqual(self.heap._heapified_heap_low(), [25, 20, 15, 15, 16, 7, 14, 5])
        self.heap._push_to_heap_low(77)
        self.assertListEqual(self.heap.heap_low, [77,    25, 15,     20, 16, 7, 14,     5, 15])
        self.assertListEqual(self.heap._heapified_heap_low(), [77,    25, 15,     20, 16, 7, 14,     5, 15])
        self.heap._push_to_heap_low(96)
        self.assertListEqual(self.heap.heap_low, [96,    77, 15,    20, 25, 7, 14,     5, 15, 16])
        self.assertListEqual(self.heap._heapified_heap_low(), [96,    77, 15,    20, 25, 7, 14,     5, 15, 16])

    def test_push_to_heap_high(self):
        self.heap._push_to_heap_high(5)
        self.assertListEqual(self.heap.heap_high, [5])
        self.heap._push_to_heap_high(20)
        self.assertListEqual(self.heap.heap_high, [5, 20])
        self.heap._push_to_heap_high(7)
        self.assertListEqual(self.heap.heap_high, [5, 20, 7])
        self.heap._push_to_heap_high(3)
        self.assertListEqual(self.heap.heap_high, [3, 5, 7, 20])
        self.heap._push_to_heap_high(16)
        self.assertListEqual(self.heap.heap_high, [3, 5, 7, 20, 16])
        self.heap._push_to_heap_high(14)
        self.assertListEqual(self.heap.heap_high, [3, 5, 7, 20, 16, 14])
        self.heap._push_to_heap_high(15)
        self.assertListEqual(self.heap.heap_high, [3, 5, 7, 20, 16, 14, 15])
        self.heap._push_to_heap_high(15)
        self.assertListEqual(self.heap.heap_high, [3, 5, 7, 15, 16, 14, 15, 20])

    def test_heappush(self):
        self.heap.heappush(5)
        self.assertListEqual(self.heap.heap_high, [5])
        self.assertEqual(self.heap.median(), 5)
        self.heap.heappush(2)
        self.assertListEqual(self.heap.heap_low, [2])
        self.assertEqual(self.heap.median(), 2)
        self.heap.heappush(3)
        self.assertListEqual(self.heap.heap_low, [2])
        self.assertListEqual(self.heap.heap_high, [3, 5])
        self.assertEqual(self.heap.median(), 3)
        self.heap.heappush(4)
        self.assertListEqual(self.heap.heap_low, [3, 2])
        self.assertListEqual(self.heap.heap_high, [4, 5])
        self.assertEqual(self.heap.median(), 3)
        self.heap.heappush(1)
        self.assertListEqual(self.heap.heap_low, [3, 2, 1])
        self.assertListEqual(self.heap.heap_high, [4, 5])
        self.assertEqual(self.heap.median(), 3)
        self.heap.heappush(7)
        self.assertListEqual(self.heap.heap_low, [3, 2, 1])
        self.assertListEqual(self.heap.heap_high, [4, 5, 7])
        self.assertEqual(self.heap.median(), 3)
        self.heap.heappush(9)
        self.assertListEqual(self.heap.heap_low, [3, 2, 1])
        self.assertListEqual(self.heap.heap_high, [4, 5, 7, 9])
        self.assertEqual(self.heap.median(), 4)
        self.heap.heappush(4)
        self.assertListEqual(self.heap.heap_low, [4, 3, 1, 2])
        self.assertListEqual(self.heap.heap_high, [4, 5, 7, 9])
        self.assertEqual(self.heap.median(), 4)
        self.heap.heappush(3)
        self.assertListEqual(self.heap.heap_low, [4, 3, 1, 2, 3])
        self.assertListEqual(self.heap.heap_high, [4, 5, 7, 9])
        self.assertEqual(self.heap.median(), 4)
        self.heap.heappush(6)
        self.assertListEqual(self.heap.heap_low, [4, 3, 1, 2, 3])
        self.assertListEqual(self.heap.heap_high, [4, 5, 7, 9, 6])
        self.assertEqual(self.heap.median(), 4)
        self.heap.heappush(10)
        self.assertListEqual(self.heap.heap_low, [4, 3, 1, 2, 3])
        self.assertListEqual(self.heap.heap_high, [4, 5, 7, 9, 6, 10])
        self.assertEqual(self.heap.median(), 4)

    def test_median(self):
        self.assertEqual(self.heap.median(), 0)
        self.heap.heap_low = [5]
        self.assertEqual(self.heap.median(), 5)
        self.heap = Median()
        self.heap.heap_high = [5]
        self.assertEqual(self.heap.median(), 5)
        self.heap = Median()
        self.heap.heap_low = [5]
        self.heap.heap_high = [6]
        self.assertEqual(self.heap.median(), 5)
        self.heap.heap_low = [6, 5]
        self.heap.heap_high = [7]
        self.assertEqual(self.heap.median(), 6)
        self.heap.heap_low = [6, 5]
        self.heap.heap_high = [7, 8]
        self.assertEqual(self.heap.median(), 6)
        self.heap.heap_low = [6, 5]
        self.heap.heap_high = [7, 8, 9]
        self.assertEqual(self.heap.median(), 7)

    def test_balance(self):
        self.heap.heap_low = [5, 4, 3, 2, 1]
        self.heap._balance()
        self.assertListEqual(self.heap.heap_low, [3, 2, 1])
        self.assertListEqual(self.heap.heap_high, [4, 5])

    def test_heappushmedian(self):
        input_and_median = [(6321, 6321), (2445, 2445), (1234, 2445), (1555, 1555)]
        for input, expected_median in input_and_median:
            median = self.heap.heappushmedian(input)
            self.assertEqual(median, expected_median)

    def test_input(self):
        input = [6331, 2793, 1640, 9290, 225, 625, 6195, 2303, 5685, 1354]
        expected = [6331, 2793, 2793, 2793, 2793, 1640, 2793, 2303, 2793]
        for i, expected_median in zip(input, expected):
            median = self.heap.heappushmedian(i)
            self.assertEqual(median, expected_median, "heap median expected %r but got %r" % (expected_median, median))

if __name__ == '__main__':
    unittest.main()
