import heapq
import unittest
from collections import deque

from huffman import (Node, encode_huffman, get_huffman_min_max_code_length,
                     parse_file, parse_input)

TEST_INPUT_FILE = 'test_input_file.txt'


class TestHuffman(unittest.TestCase):

    def test_parse_file(self):
        parsed_file = parse_file(TEST_INPUT_FILE)
        self.assertIsInstance(parsed_file, list)
        self.assertEqual(len(parsed_file), 6)
        self.assertIsInstance(parsed_file[0], str)
        self.assertIsInstance(parsed_file[1], str)
        self.assertIsInstance(parsed_file[2], str)
        self.assertEqual(parsed_file[0], '5')
        self.assertEqual(parsed_file[1], '1')
        self.assertEqual(parsed_file[2], '5')

    def test_parse_input(self):
        parsed_file = parse_file(TEST_INPUT_FILE)
        parsed_input = parse_input(parsed_file)
        self.assertIsInstance(parsed_input['num_nodes'], int)
        self.assertIsInstance(parsed_input['nodes'], list)
        self.assertIsInstance(parsed_input['nodes'][0], tuple)
        self.assertTrue(len(parsed_input['nodes'][0]), 2)
        self.assertIsInstance(parsed_input['nodes'][0][0], int)
        self.assertIsInstance(parsed_input['nodes'][0][1], Node)
        self.assertEqual(parsed_input['nodes'][0][0], 1)
        self.assertEqual(parsed_input['nodes'][0][1].weight, 1)
        self.assertEqual(parsed_input['nodes'][0][1].idx, 1)
        self.assertEqual(len(parsed_input['nodes']), len(parsed_file) - 1)

    def test_parse_input_big(self):
        parsed_file = [
            '5',
            '1',
            '5',
            '7',
            '2',
            '9',
        ]
        parsed_input = parse_input(parsed_file)
        self.assertIsInstance(parsed_input['num_nodes'], int)
        self.assertEqual(parsed_input['num_nodes'], 5)
        self.assertIsInstance(parsed_input['nodes'], list)
        self.assertIsInstance(parsed_input['nodes'][0], tuple)
        self.assertTrue(len(parsed_input['nodes'][0]), 2)
        self.assertIsInstance(parsed_input['nodes'][0][0], int)
        self.assertIsInstance(parsed_input['nodes'][0][1], Node)
        self.assertEqual(len(parsed_input['nodes']), len(parsed_file) - 1)
        expected = [
            (1, Node(weight=1, idx=1)),
            (2, Node(weight=2, idx=4)),
            (5, Node(weight=5, idx=2)),
            (7, Node(weight=7, idx=3)),
            (9, Node(weight=9, idx=5)),
        ]
        for idx, node_pair in enumerate(expected):
            expected_weight, expected_node = node_pair
            heapq.heapify(parsed_input['nodes'])
            test_node_weight, test_node = heapq.heappop(parsed_input['nodes'])
            self.assertEqual(expected_weight, test_node_weight)
            self.assertEqual(test_node.idx, expected_node.idx)
            self.assertEqual(test_node.weight, expected_node.weight)

    def test_encode_huffman(self):
        parsed_file = parse_file(TEST_INPUT_FILE)
        parsed_input = parse_input(parsed_file)
        root_node = encode_huffman(parsed_input)
        self.assertEqual(root_node.left.idx, None)
        self.assertEqual(root_node.left.weight, 15)
        self.assertEqual(root_node.left.depth, 1)
        self.assertEqual(root_node.right.idx, 5)
        self.assertEqual(root_node.right.weight, 9)
        self.assertEqual(root_node.right.depth, 1)

    def test_encode_big_huffman(self):
        parsed_file = [
            '5',
            '1',
            '5',
            '7',
            '2',
            '9',
        ]
        expected_tree = Node(
            weight=24,
            left=Node(
                weight=15,
                left=Node(
                    weight=8,
                    left=Node(weight=5, idx=2),
                    right=Node(
                        weight=3,
                        left=Node(weight=2, idx=4),
                        right=Node(weight=1, idx=1),
                    ),
                ),
                right=Node(weight=7, idx=3),
            ),
            right=Node(weight=9, idx=4),
        )
        parsed_input = parse_input(parsed_file)
        node = encode_huffman(parsed_input)
        q = deque([(node, expected_tree)])
        while q:
            node, expected_node = q.popleft()
            if node.left or node.right:
                if node.left:
                    q.append((node.left, expected_node.left))
                if node.right:
                    q.append((node.right, expected_node.right))
        for node_pair in q:
            returned_node, expected_node = node_pair[0], node_pair[1]
            self.assertIsInstance(returned_node, expected_node)
            self.assertEqual(returned_node.weight, expected_node.weight)
            self.assertEqual(returned_node.idx, expected_node.idx)
            self.assertIsInstance(returned_node.left, (Node, None))
            self.assertIsInstance(returned_node.right, (Node, None))
            if returned_node.idx:
                self.assertIsNone(returned_node.left)
                self.assertIsNone(returned_node.right)
            if returned_node.left is None and returned_node.right is None:
                self.assertIsNone(returned_node.idx)
            if returned_node.idx == 24:
                self.assertEqual(returned_node.left.weight, 15)
                self.assertEqual(returned_node.right.weight, 9)
            elif returned_node.idx == 15:
                self.assertEqual(returned_node.left.weight, 8)
                self.assertEqual(returned_node.right.weight, 8)
                self.assertEqual(returned_node.parent.weight, 24)
            elif returned_node.idx == 8:
                self.assertEqual(returned_node.left.weight, 5)
                self.assertEqual(returned_node.right.weight, 3)
                self.assertEqual(returned_node.parent.weight, 15)
            elif returned_node.idx == 3:
                self.assertEqual(returned_node.left.weight, 2)
                self.assertEqual(returned_node.right.weight, 1)
                self.assertEqual(returned_node.parent.weight, 8)

    def test_get_huffman_min_code_length(self):
        parsed_file = [
            '5',
            '1',
            '5',
            '7',
            '2',
            '9',
        ]
        parsed_input = parse_input(parsed_file)
        root_node = encode_huffman(parsed_input)
        min_code_length = get_huffman_min_max_code_length(root_node)
        self.assertEqual(min_code_length, 1)

    def test_get_huffman_max_code_length(self):
        parsed_file = [
            '5',
            '1',
            '5',
            '7',
            '2',
            '9',
        ]
        parsed_input = parse_input(parsed_file)
        root_node = encode_huffman(parsed_input)
        max_code_length = get_huffman_min_max_code_length(root_node, min=False)
        self.assertEqual(max_code_length, 4)

    def test_huffman_min_max_example_1(self):
        parsed_file = [
            10,
            37,
            59,
            43,
            27,
            30,
            96,
            96,
            71,
            8,
            76,
        ]
        parsed_input = parse_input(parsed_file)
        root_node = encode_huffman(parsed_input)
        min_code_length = get_huffman_min_max_code_length(root_node)
        self.assertEqual(min_code_length, 2)
        max_code_length = get_huffman_min_max_code_length(root_node, min=False)
        self.assertEqual(max_code_length, 5)

    def test_huffman_min_max_example_2(self):
        parsed_file = [
            15,
            895,
            121,
            188,
            953,
            378,
            849,
            153,
            579,
            144,
            727,
            589,
            301,
            442,
            327,
            930,
        ]
        parsed_input = parse_input(parsed_file)
        root_node = encode_huffman(parsed_input)
        min_code_length = get_huffman_min_max_code_length(root_node)
        self.assertEqual(min_code_length, 3)
        max_code_length = get_huffman_min_max_code_length(root_node, min=False)
        self.assertEqual(max_code_length, 6)


if __name__ == '__main__':
    unittest.main()
