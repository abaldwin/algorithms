import heapq
from collections import deque


class Node(object):
    def __init__(self, idx=None, weight=None, left=None, right=None, parent=None, depth=0):
        self.idx = idx
        self.weight = weight
        self.left = left
        self.right = right
        self.parent = parent
        self._depth = depth

    @property
    def depth(self):
        depth = 0
        node = self
        while node.parent:
            depth += 1
            node = node.parent
        return depth

    def __repr__(self):
        return "Node(idx=%r, weight=%r, left=%r, right=%r)" % (self.idx, self.weight, self.left, self.right)

    def __lt__(self, other):
        return self.weight < other.weight


def parse_file(path):
    lines = []
    try:
        with open(path, 'r') as f:
            lines = [l.strip() for l in f.readlines()]

        return lines
    except Exception as e:
        print("Error reading file")
    return lines

def parse_input(parsed_file):
    result = {
        'num_nodes': 0,
        'nodes': [],
    }
    if not parsed_file:
        return result
    result['num_nodes'], nodes = int(parsed_file[0]), parsed_file[1:]
    for idx, weight in enumerate(nodes):
        result['nodes'].append((int(weight), Node(idx=(idx + 1), weight=int(weight))))
    heapq.heapify(result['nodes'])
    return result

def encode_huffman(input_tree):
    num_nodes = input_tree['num_nodes']
    nodes = input_tree['nodes']
    result = None
    if num_nodes <= 0:
        return result
    _, right_node = heapq.heappop(nodes)
    try:
        while nodes and len(nodes) >= 1:
            try:
                try:
                    heapq.heapify(nodes)
                except Exception as e:
                    print("Error heapifying: %r" % e)
                try:
                    _, left_node = heapq.heappop(nodes)
                except Exception as e:
                    print("Error heap popping: %r" % e)
                if left_node:
                    try:
                        left_node, right_node = (left_node, right_node) if left_node.weight > right_node.weight else (right_node, left_node)
                    except Exception as e:
                        print("Error doing compare: %r" % e)
                    merge_node = Node(
                        weight=left_node.weight + right_node.weight,
                        left=left_node,
                        right=right_node,
                    )
                    left_node.parent = merge_node
                    right_node.parent = merge_node
                    try:
                        heapq.heappush(nodes, (merge_node.weight, merge_node))
                    except Exception as e:
                        print("Error heap pushing: %r" % e)
                    _, right_node = heapq.heappop(nodes)
            except Exception as e:
                print("Error encoding inner huffman: %r" % e)
    except Exception as e:
        print("Error encoding huffman: %r" % e)
    return right_node

def get_huffman_min_max_code_length(root_node, min=True):
    q = deque([root_node])
    best_depth = float('inf') if min else float('-inf')
    while q:
        node = q.popleft()
        if node.idx:
            node_depth_is_better_than_best = (node.depth < best_depth) if min else (node.depth >= best_depth)
            if node_depth_is_better_than_best:
                best_depth = node.depth
        if node.left or node.right:
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
    return best_depth

if __name__ == '__main__':
    parsed_file = parse_file('huffman.txt')
    parsed_input = parse_input(parsed_file)
    root_node = encode_huffman(parsed_input)
    print("Min code length: %r" % get_huffman_min_max_code_length(root_node))
    print("Max code length: %r" % get_huffman_min_max_code_length(root_node, min=False))
