import heapq
import random
from collections import defaultdict


def get_mst(edges):
    V = set(edges.keys())
    V_X = set(V)
    v = V_X.pop()
    X = set([v])
    h = []
    for edge in edges.get(v):
        if edge[1] not in X:
            heapq.heappush(h, (edge[0], edge[1]))
    T = []
    while X != V:
        min_edge = heapq.heappop(h)
        while min_edge[1] in X:
            min_edge = heapq.heappop(h)
        T.append(min_edge[0])
        X.add(min_edge[1])
        v = min_edge[1]
        for edge in edges.get(v):
            if edge[1] not in X:
                heapq.heappush(h, (edge[0], edge[1]))
    return T

def sum_mst(mst_input):
    return sum(mst_input)

if __name__ == '__main__':
    with open('edges.txt') as f:
        num_nodes = f.readline().strip().split()
        num_nodes, num_edges = int(num_nodes[0]), int(num_nodes[1])
        input_edges = [j.strip().split(' ') for j in f.readlines()]
        edges = defaultdict(list)
        for v1, v2, e_cost in input_edges:
            edges[int(v1)].append((int(e_cost), int(v2)))
            edges[int(v2)].append((int(e_cost), int(v1)))
        print(sum_mst(get_mst(edges)))
