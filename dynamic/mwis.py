from collections import defaultdict


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

def parse_file(path):
    lines = []
    try:
        with open(path, 'r') as f:
            lines = [l.strip() for l in f.readlines()]
    except Exception as e:
        print("Error reading file")
    return lines

def parse_input(parsed_file, includes_num_nodes=True):
    result = {}
    if not parsed_file:
        return result

    if includes_num_nodes:
        nodes_to_parse = [int(n) for n in parsed_file[1:]]
        num_nodes = int(parsed_file[0])
    else:
        nodes_to_parse = [int(n) for n in parsed_file[:]]
        num_nodes = len(nodes_to_parse)
    result = {
        'num_nodes': num_nodes,
        'nodes': [],
    }
    for idx, weight in enumerate(nodes_to_parse, start=1):
        result['nodes'].append((int(weight), idx))
    return result

def get_mwis(input_tree):
    """Get minimum weight independent set
    """
    num_nodes = input_tree['num_nodes']
    nodes = input_tree['nodes']
    if num_nodes <= 0:
        return []
    weights = [0, nodes[0][0]]
    for idx, node_pair in enumerate(nodes[1:], start=1):
        node_weight, node_idx = node_pair
        wis_prime = weights[idx]
        prime2_index = max(1, idx) - 1
        wis_prime2 = weights[prime2_index] + node_weight
        weights.append(max(wis_prime, wis_prime2))
    return weights

def nodes_in_solution(input_nodes, mwis):
    """Get the nodes in the minimum weight independent set
    """
    i = len(mwis)
    in_val = set()
    while i >= 1:
        wis_prime = mwis[i - 2]
        wis_prime2 = mwis[i - 1]
        if wis_prime >= wis_prime2:
            i -= 1
        else:
            # vertex_weight = wis_prime2 - mwis[max(i - 3, 0)]
            vertex = i - 1
            in_val.add(vertex)
            i -= 2
    return ''.join([str(int(n in in_val)) for n in input_nodes])

if __name__ == '__main__':
    parsed_file = parse_file('mwis.txt')
    parsed_input = parse_input(parsed_file)
    mwis = get_mwis(parsed_input)
    result = nodes_in_solution([1, 2, 3, 4, 17, 117, 517, 997], mwis)
    print(result)