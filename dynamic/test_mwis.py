import unittest

from mwis import parse_file, parse_input, get_mwis, Node, nodes_in_solution


TEST_INPUT_FILE = 'test_input_file.txt'


class TestMwis(unittest.TestCase):
    def test_parse_file(self):
        parsed_file = parse_file(TEST_INPUT_FILE)
        self.assertIsInstance(parsed_file, list)
        self.assertEqual(len(parsed_file), 8)
        self.assertIsInstance(parsed_file[0], str)
        self.assertIsInstance(parsed_file[1], str)
        self.assertIsInstance(parsed_file[2], str)
        self.assertEqual(parsed_file[0], '7')
        self.assertEqual(parsed_file[1], '3')
        self.assertEqual(parsed_file[2], '4')

    def test_parse_input(self):
        parsed_file = parse_file(TEST_INPUT_FILE)
        parsed_input = parse_input(parsed_file)
        self.assertIsInstance(parsed_input['num_nodes'], int)
        self.assertIsInstance(parsed_input['nodes'], list)
        self.assertIsInstance(parsed_input['nodes'][0], tuple)
        self.assertTrue(len(parsed_input['nodes'][0]), 2)
        self.assertIsInstance(parsed_input['nodes'][0][0], int)
        self.assertIsInstance(parsed_input['nodes'][0][1], int)
        self.assertEqual(parsed_input['nodes'][0][0], 3)
        self.assertEqual(parsed_input['nodes'][0][1], 1)
        self.assertEqual(len(parsed_input['nodes']), len(parsed_file) - 1)

    def test_get_mwis(self):
        parsed_file = parse_file(TEST_INPUT_FILE)
        parsed_input = parse_input(parsed_file)
        mwis = get_mwis(parsed_input)
        self.assertEqual(mwis[-1], 17)

    def test_get_mwis_two(self):
        parsed_file = [2, 2, 3]
        parsed_input = parse_input(parsed_file)
        mwis = get_mwis(parsed_input)
        self.assertListEqual(mwis, [0, 2, 3])
        self.assertEqual(mwis[-1], 3)

    def test_get_nodes_in_mis_two(self):
        parsed_file = [2, 2, 3]
        parsed_input = parse_input(parsed_file)
        mwis = get_mwis(parsed_input)
        self.assertListEqual(mwis, [0, 2, 3])
        result = nodes_in_solution(parsed_file[1:], mwis)
        self.assertEqual(result, '01')

    def test_get_mwis_three(self):
        parsed_file = [3, 2, 3, 2]
        parsed_input = parse_input(parsed_file)
        mwis = get_mwis(parsed_input)
        self.assertListEqual(mwis, [0, 2, 3, 4])
        self.assertEqual(mwis[-1], 4)

    def test_get_nodes_in_mis_three(self):
        parsed_file = [3, 2, 3, 2]
        parsed_input = parse_input(parsed_file)
        mwis = get_mwis(parsed_input)
        self.assertListEqual(mwis, [0, 2, 3, 4])
        result = nodes_in_solution(parsed_file[1:], mwis)
        self.assertEqual(result, '101')

    def test_nodes_in_mwis(self):
        parsed_file = [7, 3, 4, 5, 8, 2, 5, 4]
        parsed_input = parse_input(parsed_file)
        mwis = get_mwis(parsed_input)
        import ipdb; ipdb.set_trace()
        result = nodes_in_solution(parsed_file[1:], mwis)
        self.assertEqual(result, '0101010')

    def test_get_mwis_example_1(self):
        parsed_file = [
            10,
            280,
            618,
            762,
            908,
            409,
            34,
            59,
            277,
            246,
            779,
        ]
        parsed_input = parse_input(parsed_file)
        mwis = get_mwis(parsed_input)
        result = nodes_in_solution(parsed_file[1:], mwis)
        self.assertEqual(result, '0101010101')
        self.assertEqual(mwis[-1], 2616)

    def test_get_mwis_example_2(self):
        parsed_file = [
            10,
            460,
            250,
            730,
            63,
            379,
            638,
            122,
            435,
            705,
            84,
        ]
        parsed_input = parse_input(parsed_file)
        mwis = get_mwis(parsed_input)
        result = nodes_in_solution(parsed_file[1:], mwis)
        self.assertEqual(result, '1010010010')
        self.assertEqual(mwis[-1], 2533)

if __name__ == '__main__':
    unittest.main()
