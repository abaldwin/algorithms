import unittest

import numpy as np

from knapsack import calc_knapsack, parse_input


class TestKnapsack(unittest.TestCase):
    """Test knapsack algorithm
    """
    def test_parse_input(self):
        parsed_file = ["20 5", "3 4", "2 1", "5 1", "7 4", "9 8"]
        parsed_input = parse_input(parsed_file)
        self.assertEqual(parsed_input['max_capacity'], 20)
        self.assertEqual(parsed_input['num_items'], 5)
        self.assertListEqual(parsed_input['items'], [(3, 4), (2, 1), (5, 1), (7, 4), (9, 8)])

    def test_knapsack_example_1(self):
        parsed_file = ["8 6", "1 1", "2 3", "5 4", "5 2", "4 2", "1 5"]
        parsed_input = parse_input(parsed_file)
        largest_value, values = calc_knapsack(parsed_input)
        self.assertEqual(largest_value, 14)

    def test_knapsack_example_2(self):
        parsed_file = [
            "200009190 10",
            "10 100001001",
            "20 150001010",
            "25 180001011",
            "21 70000201",
            "15 80000202",
            "30 40000310",
            "36 10000430",
            "27 120000101",
            "19 30000104",
            "7 140000203",
        ]
        parsed_input = parse_input(parsed_file)
        largest_value, values = calc_knapsack(parsed_input)
        self.assertEqual(largest_value, 112)

    def test_knapsack_example_3(self):
        parsed_file = ["6 4", "3 4", "2 3", "4 2", "4 3"]
        parsed_input = parse_input(parsed_file)
        largest_value, values = calc_knapsack(parsed_input)
        self.assertEqual(largest_value, 8)


if __name__ == '__main__':
    unittest.main()
