from collections import defaultdict, namedtuple
from multiprocessing import Pool

import numpy as np

Item = namedtuple('Item', 'value weight')


def parse_file(path):
    lines = []
    try:
        with open(path, 'r') as f:
            lines = [l.strip() for l in f.readlines()]
    except Exception as e:
        print("Error reading file")
    return lines

def parse_input(parsed_file):
    parsed_input = {}
    if not parsed_file:
        return parsed_input

    max_capacity, num_items = parsed_file[0].strip().split(' ')
    max_capacity, num_items = int(max_capacity), int(num_items)
    items_to_parse = [n.strip().split() for n in parsed_file[1:]]
    items_to_parse = [Item(value=int(v), weight=int(w)) for v, w in items_to_parse]

    parsed_input = {
        'num_items': num_items,
        'items': items_to_parse,
        'max_capacity': max_capacity,
    }
    return parsed_input


def calc_knapsack(parsed_input):
    max_capacity = parsed_input['max_capacity']
    num_items = parsed_input['num_items']
    items = parsed_input['items']
    min_item_weight = min(item.weight for item in items)
    max_capacity_plus_one = max_capacity + 1
    num_items_plus_one = num_items + 1
    values_with_zero_items = np.zeros(max_capacity_plus_one).reshape((max_capacity_plus_one, 1))
    # print("values_with_zero_items", values_with_zero_items.shape)
    values = {}
    # print("max_capacity", max_capacity)
    # print("num_items", num_items)
    # print("shape", values.shape)
    for i, item in enumerate(items, start=1):
        last_item_idx = i - 1
        try:
            del values[last_item_idx - 1]
        except:
            pass
        # print("last_item_idx =", last_item_idx)
        print("%r of %r" % (i, num_items))
        for available_capacity in range(min_item_weight, max_capacity_plus_one):
            # print("available_capacity", available_capacity)
            # print(values)
            value_without = values.get(last_item_idx, {}).get(available_capacity, 0)
            if available_capacity - item.weight < 0:
                # print("weight exceeded capacity", available_capacity - item.weight)
                if value_without != 0:
                    if i not in values:
                        values[i] = {}
                    values[i][available_capacity] = value_without
                # print("set coord %r to %r" % (coord, value_without))
            else:
                weight_without = available_capacity - item.weight
                # print("weight_without", weight_without)
                # print("last_item_idx", last_item_idx)
                value_with = values.get(last_item_idx, {}).get(weight_without, 0) + item.value
                # print("value_without", value_without)
                # print("value_with", value_with)
                if i not in values:
                    values[i] = {}
                values[i][available_capacity] = max(value_without, value_with)
                # print("set coord %r to %r" % (coord, values[available_capacity, i]))
    try:
        from pprint import pprint
        largest_value = values.get(num_items, {}).get(max_capacity)
    except:
        print("ERROR WITH DIMENSION")
        try:
            largest_value = values.get(num_items - 1, {}).get(max_capacity)
        except:
            pass
    return largest_value, values


if __name__ == '__main__':
    parsed_file = parse_file('knapsack1.txt')
    parsed_input = parse_input(parsed_file)
    largest_value, values = calc_knapsack(parsed_input)
    print(largest_value)
