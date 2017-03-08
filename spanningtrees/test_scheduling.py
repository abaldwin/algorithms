import unittest
from scheduling import schedule, get_weighted_completion_times, DIFF_SORT, RATIO_SORT




class TestScheduling(unittest.TestCase):

    def test_get_weighted_completion_times_with_diff_sort(self):
        input = {
            'num_jobs': 4,
            'jobs': [(2, 1), (8, 5), (5, 3), (3, 2)],
        }
        scheduled_jobs = schedule(input, DIFF_SORT)
        result = get_weighted_completion_times(scheduled_jobs)
        self.assertEqual(result, 40+40+30+22)

    def test_scheduling_with_diff_sort(self):
        input = {
            'num_jobs': 4,
            'jobs': [(2, 1), (8, 5), (5, 3), (3, 2)],
        }
        scheduled_jobs = schedule(input, DIFF_SORT)
        self.assertListEqual(scheduled_jobs, [(8, 5), (5, 3), (3, 2), (2, 1)])

    def test_scheduling_with_ratio_sort(self):
        input = {
            'num_jobs': 4,
            'jobs': [(2, 1), (8, 5), (5, 3), (3, 2)],
        }
        scheduled_jobs = schedule(input, RATIO_SORT)
        self.assertListEqual(scheduled_jobs, [(2, 1), (5, 3), (8, 5), (3, 2)])

    def test_get_weighted_completion_times_with_ratio_sort(self):
        input = {
            'num_jobs': 4,
            'jobs': [(2, 1), (8, 5), (5, 3), (3, 2)],
        }
        scheduled_jobs = schedule(input, RATIO_SORT)
        result = get_weighted_completion_times(scheduled_jobs)
        self.assertEqual(result, 2+20+72+33)

if __name__ == '__main__':
    unittest.main()
