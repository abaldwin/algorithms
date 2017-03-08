import unittest
from count_split_inversions import count_inversions


class TestCountSplitInversions(unittest.TestCase):

    def test_count_inversions(self):
        input = [1, 3, 5, 2, 4, 6]
        result = count_inversions(input)
        self.assertEqual(result, 3)

if __name__ == '__main__':
    unittest.main()
