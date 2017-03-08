import unittest
from mst import get_mst, sum_mst


class TestMst(unittest.TestCase):

    def test_get_mst_sum(self):
        input_edges = {
            1: [(3, 2), (8, 5), (2, 6)],
            2: [(2, 5), (9, 6), (3, 1)],
            5: [(2, 2)],
            6: [(9, 2), (2, 1)],
        }
        result = sum_mst(get_mst(input_edges))
        self.assertEqual(result, 7)

if __name__ == '__main__':
    unittest.main()
