"""PAINTING GRAPH"""
def is_bipartite(ghraph: dict) -> bool:
    """
    Checks whether the underlying undirected graph is bipartite using BFS coloring.

    The function attempts to color each node using two colors ('1' and '2').
    A graph is bipartite if no two adjacent nodes have the same color.
    It first constructs the underlying undirected graph from the input
    (which may be oriented or undirected) by adding reciprocal edges.

    Parameters
    ----------
    graph : dict
        A dictionary mapping each node (integer) to a list of its neighbors.

    Returns
    -------
    bool
        True if the graph is bipartite, False otherwise.

    Doctests
    --------
    >>> is_bipartite({})          # empty graph
    True

    >>> is_bipartite({1: []})     # single node
    True

    >>> is_bipartite({            # simple chain 1 - 2 - 3 (undirected input)
    ...     1: [2],
    ...     2: [1, 3],
    ...     3: [2]
    ... })
    True

    >>> is_bipartite({            # even cycle: 1-2-3-4-1 (undirected input)
    ...     1: [2, 4],
    ...     2: [1, 3],
    ...     3: [2, 4],
    ...     4: [1, 3]
    ... })
    True

    >>> is_bipartite({            # odd cycle: 1-2-3-1 (undirected input)
    ...     1: [2, 3],
    ...     2: [1, 3],
    ...     3: [1, 2]
    ... })
    False

    >>> is_bipartite({            # oriented odd cycle: 1 -> 2 -> 3 -> 1
    ...     1: [2],
    ...     2: [3],
    ...     3: [1]
    ... })
    False
    """
    adj = {node: set(neighbors) for node, neighbors in ghraph.items()}

    all_nodes = set(ghraph.keys())
    for neighbors in ghraph.values():
        all_nodes.update(neighbors)

    for node in all_nodes:
        if node not in adj:
            adj[node] = set()

    for u in ghraph:
        for v in ghraph[u]:
            adj[v].add(u)

    adj = {node: list(neighbors) for node, neighbors in adj.items()}

    color = {}
    queue = []
    #BFS
    for node in adj:
        if node not in color:
            queue = [node]
            color[node] = '1'

            while queue:
                current_node = queue.pop(0)
                for adjacent in adj.get(current_node, []):
                    if adjacent not in color:
                        if color[current_node] == '1':
                            color[adjacent] = '2'
                        elif color[current_node] == '2':
                            color[adjacent] = '1'
                        queue.append(adjacent)
                    else:
                        if color[current_node] == color[adjacent]:
                            return False
    return True

def three_coloring(graph: dict) -> list:
    """
    Attempts to find a 3-coloring for the underlying undirected graph.

    The function uses Depth-First Search (DFS) with backtracking to assign
    one of three colors ('r', 'b', 'g') to each node such that no two
    adjacent nodes share the same color. It first converts the input (which
    may be oriented) into its underlying undirected graph.

    Parameters
    ----------
    graph : dict
        A dictionary where keys are nodes and values are lists of adjacent nodes.

    Returns
    -------
    list[tuple] | str
        A list of (node, color) pairs if coloring is possible, otherwise
        "Impossible to paint".

    Doctests
    --------
    >>> three_coloring({})              # empty graph
    []

    >>> three_coloring({1: []})         # one node
    [(1, 'r')]

    >>> result = three_coloring({       # path: 1 - 2 - 3 (undirected input)
    ...     1: [2],
    ...     2: [1, 3],
    ...     3: [2]
    ... })
    >>> len(result)
    3
    >>> all(color in {'r', 'b', 'g'} for _, color in result)
    True

    >>> result = three_coloring({       # triangle: 1-2-3 fully connected (undirected input)
    ...     1: [2, 3],
    ...     2: [1, 3],
    ...     3: [1, 2]
    ... })
    >>> len(result)
    3
    >>> all(color in {'r', 'b', 'g'} for _, color in result)
    True

    >>> three_coloring({                # K4 – 4 fully connected nodes → impossible
    ...     1: [2, 3, 4],
    ...     2: [1, 3, 4],
    ...     3: [1, 2, 4],
    ...     4: [1, 2, 3]
    ... })
    'Impossible to paint'

    >>> three_coloring({                # Oriented path 1 -> 2 -> 3 (Underlying graph is P3)
    ...     1: [2],
    ...     2: [3],
    ...     3: []
    ... })
    [(1, 'r'), (2, 'b'), (3, 'r')]
    """
    adj = {node: set(neighbors) for node, neighbors in graph.items()}

    all_nodes = set(graph.keys())
    for neighbors in graph.values():
        all_nodes.update(neighbors)

    for node in all_nodes:
        if node not in adj:
            adj[node] = set()

    for u in graph:
        for v in graph[u]:
            adj[v].add(u)

    adj = {node: list(neighbors) for node, neighbors in adj.items()}

    color = {item: None for item in adj} #all aren`t painted
    nodes = list(adj.keys())

    def is_to_paint(node_to_paint, color_to_try):
        """
        Check if we can safely color a node with a specific color.
        """
        for item in adj.get(node_to_paint, []):
            if color.get(item) == color_to_try:
                return False
        return True

    def paint(node_index):
        """
        DFS
        """
        if node_index == len(color): #found a complete and valid coloring of the graph
            return True
        node_to_paint = nodes[node_index]
        for color_to_try in 'rbg':
            if is_to_paint(node_to_paint, color_to_try):
                color[node_to_paint] = color_to_try
                if paint(node_index + 1): #checking for next node
                    return True
                #next interation try another color
                color[node_to_paint] = None #if we are in situation when we can`t paint any of colors`
        return False #no color matched

    if paint(0): #start painting with first node
        return [(node, color[node]) for node in nodes]
    return 'Impossible to paint'

if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
