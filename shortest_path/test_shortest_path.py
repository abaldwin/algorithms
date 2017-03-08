import unittest
from shortest_path import parse_input, get_vertices_weights, reweight_edges, get_vertices, add_johnson_start_vertex, get_bellman_ford, get_johnson, get_path, get_floyd_warshall, NEGATIVE_CYCLE, START_VERTEX
from pprint import pprint

class TestShortestPath(unittest.TestCase):

    def test_parse_input(self):
        parsed_file = [
            "5 6",
            "22 55 2",
            "22 33 4",
            "55 33 1",
            "55 18 2",
            "33 88 4",
            "18 88 2",
        ]
        expected_result = {
            'num_nodes': 5,
            'num_edges': 6,
            'edges': {
                22: {55: 2, 33: 4},
                55: {18: 2, 33: 1},
                33: {88: 4},
                18: {88: 2},
            },
            'in_edges': {
                55: {22: 2},
                33: {55: 1, 22: 4},
                18: {55: 2},
                88: {18: 2, 33: 4},
            },
        }
        parsed_input = parse_input(parsed_file)
        self.assertEqual(parsed_input['num_nodes'], expected_result['num_nodes'])
        self.assertEqual(parsed_input['num_edges'], expected_result['num_edges'])
        self.assertDictEqual(parsed_input['edges'], expected_result['edges'])
        self.assertDictEqual(parsed_input['in_edges'], expected_result['in_edges'])

    def test_bellman_ford_good(self):
        parsed_file = [
            "5 6",
            "22 55 2",
            "22 33 4",
            "55 33 1",
            "55 18 2",
            "33 88 4",
            "18 88 2",
        ]
        expected_result = {18: 4, 33: 3, 22: 0, 88: 6, 55: 2}
        parsed_input = parse_input(parsed_file)
        vertices = get_vertices(parsed_input)
        num_vertices = len(vertices)
        result = get_bellman_ford(parsed_input, vertices, num_vertices, 22)
        self.assertDictEqual(result['sssp'], expected_result)

    def test_get_path(self):
        parsed_file = [
            "5 6",
            "22 55 2",
            "22 33 4",
            "55 33 1",
            "55 18 2",
            "33 88 4",
            "18 88 2",
        ]
        expected_path = [22, 55, 18, 88]
        parsed_input = parse_input(parsed_file)
        vertices = get_vertices(parsed_input)
        num_vertices = len(vertices)
        bellman_result = get_bellman_ford(parsed_input, vertices, num_vertices, 22)
        result = get_path(parsed_input['edges'], bellman_result['paths'], 22, 88)
        self.assertListEqual(result['path'], expected_path)
        self.assertEqual(result['cost'], 6)

    def test_bellman_ford_negative_cycle(self):
        parsed_file = [
            "4 5",
            "1 2 1",
            "1 3 4",
            "2 4 2",
            "3 4 3",
            "4 1 -4",
        ]
        parsed_input = parse_input(parsed_file)
        vertices = get_vertices(parsed_input)
        num_vertices = len(vertices)
        bellman_result = get_bellman_ford(parsed_input, vertices, num_vertices, 1)
        self.assertEqual(bellman_result['sssp'], NEGATIVE_CYCLE)

    def test_floyd_warshall(self):
        parsed_file = [
            "4 5",
            "1 2 1",
            "1 3 4",
            "2 4 2",
            "3 4 3",
            "4 1 -4",
        ]
        parsed_input = parse_input(parsed_file)
        result = get_floyd_warshall(parsed_input)
        self.assertEqual(result['shortest_path'], NEGATIVE_CYCLE)

    def test_add_johnson_start_vertex(self):
        parsed_file = [
            "5 6",
            "22 55 2",
            "22 33 4",
            "55 33 1",
            "55 18 2",
            "33 88 4",
            "18 88 2",
        ]
        expected_result = {
            'num_nodes': 6,
            'num_edges': 11,
            'edges': {
                18: {88: 2},
                22: {55: 2, 33: 4},
                33: {88: 4},
                55: {18: 2, 33: 1},
                START_VERTEX: {18: 0, 22: 0, 88: 0, 33: 0, 55: 0},
            },
            'in_edges': {
                18: {55: 2, START_VERTEX: 0},
                22: {START_VERTEX: 0},
                33: {55: 1, 22: 4, START_VERTEX: 0},
                55: {22: 2, START_VERTEX: 0},
                88: {18: 2, 33: 4, START_VERTEX: 0},
            },
        }
        parsed_input = parse_input(parsed_file)
        parsed_input, vertices, num_vertices = add_johnson_start_vertex(parsed_input)
        self.assertEqual(parsed_input['num_nodes'], expected_result['num_nodes'])
        self.assertEqual(parsed_input['num_edges'], expected_result['num_edges'])
        self.assertDictEqual(parsed_input['edges'], expected_result['edges'])
        self.assertDictEqual(parsed_input['in_edges'], expected_result['in_edges'])

    def test_get_vertices_weights(self):
        parsed_file = [
            "6 7",
            "1 2 -2",
            "2 3 -1",
            "3 1 4",
            "3 24 2",
            "3 25 -3",
            "26 24 1",
            "26 25 -4",
        ]
        expected_results = {
            1: 0,
            2: -2,
            3: -3,
            24: -1,
            25: -6,
            26: 0,
            START_VERTEX: 0,
        }
        parsed_input = parse_input(parsed_file)
        parsed_input, vertices, num_vertices = add_johnson_start_vertex(parsed_input)
        bellman_ford_result = get_bellman_ford(parsed_input, vertices, num_vertices, START_VERTEX)
        vertices_weights = get_vertices_weights(parsed_input, vertices, bellman_ford_result)
        self.assertDictEqual(expected_results, vertices_weights)

    def test_reweight_edges(self):
        parsed_file = [
            "6 7",
            "1 2 -2",
            "2 3 -1",
            "3 1 4",
            "3 24 2",
            "3 25 -3",
            "26 24 1",
            "26 25 -4",
        ]
        expected_result = {
            'num_nodes': 7,
            'num_edges': 13,
            'edges': {
                1: {2: 0},
                2: {3: 0},
                3: {1: 1, 24: 0, 25: 0},
                26: {24: 2, 25: 2},
                START_VERTEX: {1: 0, 2: 0, 3: 0, 24: 0, 25: 0, 26: 0},
            },
            'in_edges': {
                1: {3: 1, START_VERTEX: 0},
                2: {1: 0, START_VERTEX: 0},
                3: {2: 0, START_VERTEX: 0},
                24: {3: 0, 26: 2, START_VERTEX: 0},
                25: {3: 0, 26: 2, START_VERTEX: 0},
                26: {START_VERTEX: 0},
            },
        }
        parsed_input = parse_input(parsed_file)
        parsed_input, vertices, num_vertices = add_johnson_start_vertex(parsed_input)
        bellman_ford_result = get_bellman_ford(parsed_input, vertices, num_vertices, START_VERTEX)
        vertices_weights = get_vertices_weights(parsed_input, vertices, bellman_ford_result)
        parsed_input = reweight_edges(parsed_input, vertices_weights)
        self.assertEqual(parsed_input['num_nodes'], expected_result['num_nodes'])
        self.assertEqual(parsed_input['num_edges'], expected_result['num_edges'])
        self.assertDictEqual(parsed_input['in_edges'], expected_result['in_edges'])
        self.assertDictEqual(parsed_input['edges'], expected_result['edges'])

    def test_johnson(self):
        parsed_file = [
            "6 7",
            "1 2 1",
            "1 3 4",
            "2 4 2",
            "3 4 3",
            "4 1 -2",
        ]
        parsed_input = parse_input(parsed_file)
        result = get_johnson(parsed_input)
        self.assertEqual(result, -2)

if __name__ == '__main__':
    unittest.main()