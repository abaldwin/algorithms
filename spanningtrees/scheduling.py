
DIFF_SORT = lambda job: (job[0] - job[1], job[0])
RATIO_SORT = lambda job: (job[0] / job[1], job[0])

def schedule(input_jobs, sort_key):
    num_jobs = input_jobs['num_jobs']
    sorted_jobs = sorted(input_jobs['jobs'], key=sort_key, reverse=True)
    return sorted_jobs

def get_weighted_completion_times(scheduled_jobs):
    clock = 0
    weighted_sum = 0
    for weight, length in scheduled_jobs:
        clock += length
        weighted_sum += weight * clock
    return weighted_sum

if __name__ == '__main__':
    input_jobs = {}
    with open('jobs.txt') as f:
        input_jobs = {
            'num_jobs': f.readline().strip(),
            'jobs': [j.strip().split(' ') for j in f.readlines()],
        }
        input_jobs['jobs'] = [(int(w), int(l)) for w, l in input_jobs['jobs']]
        print(input_jobs['num_jobs'])
        print(input_jobs['jobs'][:10])
    print(schedule(input_jobs, DIFF_SORT)[:10])
    print(schedule(input_jobs, RATIO_SORT)[:10])
    print(get_weighted_completion_times(schedule(input_jobs, DIFF_SORT)))
    print(get_weighted_completion_times(schedule(input_jobs, RATIO_SORT)))
