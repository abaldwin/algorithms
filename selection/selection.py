#!/usr/bin/env python3

from random import randint, shuffle


def rselect(input, ith_order_stat):
    print(ith_order_stat)
    import ipdb; ipdb.set_trace()
    shuffle(input)
    return _rselect(input, 0, len(input), ith_order_stat - 1)


def partition(input, len_input):
    last_idx = len_input - 1
    pivot_idx = randint(0, last_idx)
    pivot = input[pivot_idx]
    input[last_idx], input[pivot_idx] = input[pivot_idx], input[last_idx]
    left, right = 0, last_idx - 1
    while left <= right:
        while input[left] < pivot:
            left += 1
        while input[right] > pivot:
            right -= 1
        if left <= right:
            input[left], input[right] = input[right], input[left]
            left += 1
            right -= 1
    input[last_idx], input[left] = input[left], input[last_idx]
    for idx, num in enumerate(input):
        if idx < left - 1:
            assert(num < pivot, "%s not less than %s" % (num, pivot))
        else:
            assert(num >= pivot, "%s not greater or equal to %s" % (num, pivot))
    return left - 1

def _rselect(input, left, right, search_idx):
    if right - left <= 1:
        return input[left]

    import ipdb; ipdb.set_trace()
    print(left, right)
    pivot_idx = partition(input, right - 1)
    if pivot_idx == search_idx:
        return input[pivot_idx]
    elif pivot_idx > search_idx:
        return _rselect(input, left, pivot_idx, search_idx)
    else:
        return _rselect(input, pivot_idx, right, search_idx - pivot_idx)
