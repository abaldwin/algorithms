#!/usr/bin/env python3

import math


def closest_pair(points):
    p_x = merge_sort(points, 0)
    p_y = merge_sort(points, 1)
    return _closest_pair(p_x, p_y)

def brute_force_closest_pair(points):
    num_points = len(points)
    if num_points < 2:
        return float('inf'), (None, None)
    close_pair = None
    close_dist = float('inf')
    for i in range(0, num_points - 1):
        for j in range(i + 1, num_points):
            dist = distance(points[j], points[i])
            if dist < close_dist:
                close_dist = dist
                close_pair = (points[i], points[j])
    return close_pair

def distance(p1, p2):
    x2, x1 = p2[0], p1[0]
    y2, y1 = p2[1], p1[1]
    return math.hypot(x2 - x1, y2 - y1)

def _closest_pair(p_x, p_y):
    num_points = len(p_x)
    if num_points <= 3:
        return brute_force_closest_pair(p_x)
    mid = len(p_x) // 2
    q, r = p_x[:mid], p_x[mid:]
    q_x = q
    q_y = [point for point in p_y if point in q]
    r_x = r
    r_y = [point for point in p_y if point in r]
    p1, q1 = _closest_pair(q_x, q_y)
    p2, q2 = _closest_pair(r_x, r_y)
    delta = min(distance(p1, q1), distance(p2, q2))
    p3, q3 = _closest_split_pair(p_x, p_y, delta)
    close_pair = None
    close_dist = float('inf')
    for pair in [(p1, q1), (p2, q2), (p3, q3)]:
        dist = distance(*pair)
        if dist < close_dist:
            close_dist = dist
            close_pair = pair
    return close_pair

def _closest_split_pair(p_x, p_y, delta):
    mid = len(p_x) // 2
    x_bar = p_x[mid - 1][0]
    s_y = [p for p in p_y if x_bar - delta <= p[0] <= x_bar + delta]
    best = delta
    best_pair = None
    for i in range(0, len(s_y) - 1):
        for j in range(1, min(7, len(s_y) - i)):
            p, q = s_y[i], s_y[i + j]
            dist = distance(p, q)
            if dist <= best:
                best = dist
                best_pair = p, q
    return best_pair

def merge_sort(input, coord):
    if len(input) <= 1:
        return input

    mid = len(input) // 2
    left = input[:mid]
    right = input[mid:]

    left = merge_sort(left, coord)
    right = merge_sort(right, coord)
    return merge(left, right, coord)


def merge(left, right, coord):
    result = []
    len_left = len(left)
    len_right = len(right)
    left_idx, right_idx = 0, 0
    while left_idx < len_left and right_idx < len_right:
        if left[left_idx][coord] <= right[right_idx][coord]:
            result.append(left[left_idx])
            left_idx += 1
        else:
            result.append(right[right_idx])
            right_idx += 1

    if left_idx < len_left:
        result.extend(left[left_idx:])
    elif right_idx < len_right:
        result.extend(right[right_idx:])
    return result