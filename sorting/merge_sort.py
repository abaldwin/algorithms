#!/usr/bin/env python3

from heapq import merge as heapmerge


def merge_sort_with_heap(input):
    if len(input) <= 1:
        return input

    mid = len(input) // 2
    left = input[:mid]
    right = input[mid:]

    left = merge_sort(left)
    right = merge_sort(right)
    return list(heapmerge(left, right))


def merge_sort(input):
    if len(input) <= 1:
        return input

    middle = len(input) // 2
    left = input[:middle]
    right = input[middle:]

    left = merge_sort(left)
    right = merge_sort(right)
    return list(merge(left, right))


def merge(left, right):
    result = []
    left_idx, right_idx = 0, 0
    while left_idx < len(left) and right_idx < len(right):
        if left[left_idx] <= right[right_idx]:
            result.append(left[left_idx])
            left_idx += 1
        else:
            result.append(right[right_idx])
            right_idx += 1

    if left_idx < len(left):
        result.extend(left[left_idx:])
    if right_idx < len(right):
        result.extend(right[right_idx:])
    return result