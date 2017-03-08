#!/usr/bin/env python3

from random import shuffle


def quicksort(input):
    shuffle(input)
    return _quicksort(input, 0, len(input) - 1)


def _quicksort(input, start, stop):
    if stop - start > 0:
        pivot, left, right = input[start], start, stop
        while left <= right:
            while input[left] < pivot:
                left += 1
            while input[right] > pivot:
                right -= 1
            if left <= right:
                input[left], input[right] = input[right], input[left]
                left += 1
                right -= 1
        _quicksort(input, start, right)
        _quicksort(input, left, stop)
    return input
