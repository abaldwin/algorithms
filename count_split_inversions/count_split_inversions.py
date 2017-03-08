#!/usr/bin/env python3

inversions = 0


def count_inversions(input):
    _ = merge_sort(input)
    return inversions


def merge_sort(input):
    if len(input) <= 1:
        return input

    mid = len(input) // 2
    left = input[:mid]
    right = input[mid:]

    left = merge_sort(left)
    right = merge_sort(right)
    return merge(left, right)


def merge(left, right):
    global inversions
    result = []
    len_left, len_right = len(left), len(right)
    left_idx, right_idx = 0, 0
    while left_idx < len_left and right_idx < len_right:
        if left[left_idx] <= right[right_idx]:
            result.append(left[left_idx])
            left_idx += 1
        else:
            result.append(right[right_idx])
            right_idx += 1
            inversions += len(left[left_idx:])

    if left_idx < len_left:
        result.extend(left[left_idx:])
    elif right_idx < len_right:
        result.extend(right[right_idx:])
    return result