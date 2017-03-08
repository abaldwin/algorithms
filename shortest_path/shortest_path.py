from collections import defaultdict, deque

DEBUG = False
NEGATIVE_CYCLE = 'negative cycle'
START_VERTEX = 999999


def parse_file(path):
    """Return the lines of a file

    Args:
        path (str): The file path

    Returns:
        list: The lines in the file
    """
    if DEBUG:
        print("Parsing %r" % path)
    lines = []
    try:
        with open(path, 'r') as f:
            lines = [l.strip() for l in f.readlines()]
    except Exception as e:
        print("Error reading file")
    return lines


def parse_input(parsed_file):
    """Parse a list of strings of a known order and structure

    Args:
        parsed_file (list): The list of strings

    Returns:
        dict: A dictionary of relevant properties from the list of strings
    """
    if DEBUG:
        print("Parsing input")
    parsed_input = {}
    if not parsed_file:
        return parsed_input

    num_nodes, num_edges = parsed_file[0].strip().split()
    parsed_input['num_nodes'], parsed_input['num_edges'] = int(num_nodes), int(num_edges)

    edges_to_parse = [n.strip().split() for n in parsed_file[1:]]
    edges_to_parse = [(int(tail), int(head), int(weight)) for tail, head, weight in edges_to_parse]

    edges = defaultdict(dict)
    in_edges = defaultdict(dict)
    for tail, head, weight in edges_to_parse:
        edges[tail][head] = in_edges[head][tail] = weight

    parsed_input['edges'] = edges
    parsed_input['in_edges'] = in_edges

    return parsed_input


def get_vertices(parsed_input):
    """Get the vertices

    Args:
        parsed_input (dict): The parsed input

    Returns:
        set: All of the vertices
    """
    if DEBUG:
        print("Getting vertices")
    vertices = set(e for e in parsed_input['edges'])
    vertices = vertices.union(set(e for e in parsed_input['in_edges']))
    return vertices


def get_path(edges, paths, start, end):
    """Get the shortest path from a collection of edges

    Args:
        edges (dict): The collection of edges, with vertices as keys and connected edges and weights as the value
        paths (dict):
        start (int): The start node
        end (int): The end node

    Returns:
        dict: The found shortest path and cost of that path
    """
    result = {'cost': 0, 'path': deque([end])}
    if start == end:
        return result
    head = end
    seen = set()
    try:
        while head != start:
            tail = paths[head]
            edge_cost = edges[tail].get(head, float('inf'))
            if (tail, head) in seen:
                if result['cost'] < 0:
                    result['cost'] = NEGATIVE_CYCLE
                    return result
            seen.add((tail, head))
            if edge_cost != float('inf'):
                result['cost'] += edge_cost
                result['path'].appendleft(tail)
                head = tail
    except Exception as e:
        print("Exception: %r" % e)
        return None
    result['path'] = list(result['path'])
    return result


def get_bellman_ford(parsed_input, vertices, num_vertices, start_vertex):
    """Get the shortest path from a start vertex to all other vertices

    Args:
        parsed_input (dict): The information about graph edges and vertices
        vertices (set): The set of vertices
        num_vertices (int): The number of vertices
        start_vertex (int): The path's starting vertex

    Returns:
        dict: The single source shortest paths and the information to reconstruct the path
    """
    if DEBUG:
        print("Getting Bellman-Ford")
    in_edges = parsed_input['in_edges']

    A = defaultdict(dict)
    B = defaultdict(dict)
    for i in range(0, num_vertices):
        if DEBUG:
            if i % 100 == 0:
                print("Bellman-Ford loop: %s of %s" % (i, num_vertices))
        for v in vertices:
            if i == 0:
                A[i][v] = 0 if v == start_vertex else float('inf')
                B[i][v] = None
            else:
                best_cost = last_round_cost = A[i - 1][v]
                B[i][v] = B[i - 1][v]
                for v2, weight in in_edges[v].items():
                    cost = A[i - 1][v2] + weight
                    if cost < best_cost:
                        best_cost = cost
                        B[i][v] = v2
                A[i][v] = min(last_round_cost, best_cost)
        if i > 0 and all(A[i - 1][v] == A[i][v] for v in vertices):
            break
    if A[i][start_vertex] < 0 or (i == num_vertices and any(A[i][v] < A[i - 1][v] for v in vertices)):
        return {'sssp': NEGATIVE_CYCLE, 'paths': None}
    return {'sssp': A[i], 'paths': B[i]}


def get_floyd_warshall(parsed_input):
    """Find the shortest path in a weighted graph with positive or negative edge weights but no negative cycles

    Args:
        parsed_input (dict): The information about graph edges and vertices

    Returns:
        dict: The All-Pairs shortest path and the information to reconstruct the paths
    """
    if DEBUG:
        print("Getting Floyd-Warshall")
    edges = parsed_input['edges']
    vertices = get_vertices(parsed_input)
    num_vertices = len(vertices)

    A = defaultdict(dict)
    B = defaultdict(dict)

    for i in vertices:
        for j in vertices:
            if i == j:
                A[i][j] = 0
            else:
                A[i][j] = edges[i].get(j, float('inf'))

    for k in vertices:
        for i in vertices:
            for j in vertices:
                A[i][j] = min(A[i][j], A[i][k] + A[k][j])
                if A[i][j] == A[i][k] + A[k][j]:
                    B[i][j] = k
    if any(A[i][i] < 0 for i in vertices):
        return {'apsp': None, 'paths': None, 'shortest_path': NEGATIVE_CYCLE}
    shortest_path = [min(v for v in B[i].values()) for i in vertices][0]
    return {'apsp': A[num_vertices], 'paths': B[num_vertices], 'shortest_path': shortest_path}


def add_johnson_start_vertex(parsed_input):
    """Add a vertex to a graph that has edges to every other vertex

    Args:
        parsed_input (dict): The information about graph edges and vertices

    Returns:
        dict, set, int: The updated parsed input, set of vertices, and number of vertices
    """
    if DEBUG:
        print("Adding Johnson start vertex")
    vertices = get_vertices(parsed_input)
    num_vertices = len(vertices)

    for v in vertices:
        parsed_input['edges'][START_VERTEX][v] = 0
        parsed_input['in_edges'][v][START_VERTEX] = 0
    parsed_input['num_nodes'] += 1
    parsed_input['num_edges'] += num_vertices
    vertices.add(START_VERTEX)
    return parsed_input, vertices, num_vertices + 1


def reweight_edges(parsed_input, vertices_weights):
    """Reweight the edges of a graph to remove negative weights

    Args:
        parsed_input (dict): The information about graph edges and vertices
        vertices_weights (dict): A map of vertices to their weights

    Returns:
        dict: The updated parsed input
    """
    if DEBUG:
        print("Reweighting edges")
    edges = parsed_input['edges']
    reweighted_edges = defaultdict(dict)
    reweighted_in_edges = defaultdict(dict)
    for tail, edges in edges.items():
        for head, weight in edges.items():
            if tail == START_VERTEX:
                reweighted_edges[tail][head] = weight
                reweighted_in_edges[head][tail] = weight
            else:
                new_weight = weight + vertices_weights[tail] - vertices_weights[head]
                reweighted_edges[tail][head] = new_weight
                reweighted_in_edges[head][tail] = new_weight
    parsed_input['edges'] = reweighted_edges
    parsed_input['in_edges'] = reweighted_in_edges
    return parsed_input


def get_vertices_weights(parsed_input, vertices, bellman_ford_result):
    """Get vertices weights, used for reweighting negative edge weights as part of Johnson's algorithm

    Args:
        parsed_input (dict): The information about graph edges and vertices
        vertices (set): The set of vertices
        bellman_ford_result (dict): The single source shortest paths and information to reconstruct the paths

    Returns:
        dict: A map of vertices to their weights
    """
    if DEBUG:
        print("Getting vertices weights")
    edges = parsed_input['edges']
    vertices_weights = {}
    for v in vertices:
        vertices_weights[v] = get_path(edges, bellman_ford_result['paths'], START_VERTEX, v)['cost']
        if vertices_weights[v] == NEGATIVE_CYCLE:
            return NEGATIVE_CYCLE
    return vertices_weights


def get_dijkstra(parsed_input, vertices, dest):
    """Find the shortest path between two nodes

    Args:
        parsed_input (dict): The information about graph edges and vertices
        vertices (set): The set of vertices
        dest (int): The final node

    Returns:
        int: The cost of the shortest path between two nodes
    """
    dist = {vertex: float('inf') for vertex in vertices}
    previous = {vertex: None for vertex in vertices}
    dist[START_VERTEX] = 0
    q = vertices.copy()
    in_edges = parsed_input['in_edges']

    while q:
        head = q.pop()
        for tail, cost in in_edges[head].items():
            alt = dist[tail] + cost
            if alt < dist[head]:   # Relax (u,v,a)
                dist[head] = alt
                previous[head] = tail
    s, u, s_cost = deque(), dest, deque()
    while previous[u]:
        s.appendleft(u)
        u = previous[u]
    s.appendleft(u)
    s_cost.appendleft(dist[dest])
    return sum(s_cost)


def get_johnson(parsed_input):
    """Get all pairs shortest paths in a sparse, edge-weighted, directed graph

    Args:
        parsed_input (dict): The information about graph edges and vertices

    Returns:
        int: The cost of the shortest path
    """
    if DEBUG:
        print("Getting Johnson")
    parsed_input, vertices, num_vertices = add_johnson_start_vertex(parsed_input)

    bellman_ford_result = get_bellman_ford(parsed_input, vertices, num_vertices, START_VERTEX)
    if bellman_ford_result['sssp'] == NEGATIVE_CYCLE:
        return bellman_ford_result
    vertices_weights = get_vertices_weights(parsed_input, vertices, bellman_ford_result)
    if vertices_weights == NEGATIVE_CYCLE:
        return NEGATIVE_CYCLE
    parsed_input = reweight_edges(parsed_input, vertices_weights)
    shortest_path = float('inf')
    for idx, v in enumerate(vertices):
        if DEBUG:
            if idx % 100 == 0:
                print("Johnson loop %s of %s" % (idx, num_vertices))
        cost = get_dijkstra(parsed_input, vertices, v)
        true_cost = cost - vertices_weights[START_VERTEX] + vertices_weights[v]
        if true_cost < shortest_path:
            shortest_path = true_cost
    return shortest_path

if __name__ == '__main__':
    # Load all graphs and check for shortest length cost
    DEBUG = True
    print("Getting lengths for small graphs")
    input_files = ['g1.txt', 'g2.txt', 'g3.txt']
    for filename in input_files:
        parsed_file = parse_file(filename)
        parsed_input = parse_input(parsed_file)
        print(get_johnson(parsed_input))

    print("Getting large file")
    filename = 'large.txt'
    parsed_file = parse_file(filename)
    parsed_input = parse_input(parsed_file)
    print(get_johnson(parsed_input))