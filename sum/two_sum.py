#!/usr/bin/env python3

import numpy as np
import time
import collections

def two_sum(input):
    input_set = set(input)
    count = 0
    start = time.time()
    print(len(input))
    print(len(input_set))
    for idx, n in enumerate(input):
        if (idx % 5000 == 0):
            print("idx %r, count %r, time %r" % (idx, count, (time.time() - start) / 60))
        for t in range(-10000, 10001):
            if 2*n == t:
                continue
            n2 = t - n
            if n2 in input_set:
                count += 1
    return count // 2

def two_sum2(input):
    start = time.time()
    count = 0
    check_range = np.arange(-10000, 10001)
    for idx, i in enumerate(input):
        if (idx % 1000 == 0):
            print("idx %r, count %r, time %r" % (idx, count, (time.time() - start) / 60))
        targets = check_range - i
        count += sum(t in input for t in targets if t != i)
    return count / 2

if __name__ == '__main__':
    with open('prob-2sum.txt', 'r') as f:
        content = f.read()
    input = content.split('\n')
    input = [int(n) for n in input if len(n)]
    print(two_sum(input))
