def find_euler_cycle(graph: tuple, oriented: bool = False):
    """
    An Eulerian cycle is a path in graph theory that visits every edge of a graph exactly once
    and ends at the same vertex it started from.

    A graph has an Eulerian cycle if and only if it is connected
    (ignoring isolated vertices) and every vertex has an even degree.

    First, this function checks if the graph is connected and if every vertex has an even degree.
    Then, it builds a cycle using Hierholzer's algorithm.

    The basic idea of Hierholzer's algorithm is the stepwise construction of the Eulerian cycle
    by connecting dijunctive circles. It starts with a random node and then follows an arbitrary
    unvisited edge to a neighbour. This step is repeated until one returns to the starting node.
    This yields a first circle in the graph.

        Parameters:
            graph: tuple[dict[str, set[str]], set[tuple[str, str]]]
            (connections, edges)
            oriented : bool
        Returns:
            False : if Eulerian cycle is impossible.
            list[str] : a list of edges in order of the path (cycle)

    Tests:
    >>> find_euler_cycle(({'A': {}}, {}))
    >>> find_euler_cycle(({'A': {'B', 'E', 'C'}, 'B': {'A', 'C'}, 'C': {'B', 'D', 'A'}, \
'D': {'E', 'C'}, 'E': {'D', 'A'}}, {('E', 'D'), ('D', 'E'), ('C', 'D'), ('B', 'C'), ('D', 'C'), \
('A', 'E'), ('B', 'A'), ('E', 'A'), ('C', 'B'), ('A', 'B'), ('A', 'C'), ('C', 'A')}))
    >>> find_euler_cycle(({'A': {'B', 'C'}, 'B': {'C'}, 'C': {'D'}, 'D': {'E'}, 'E': {'A'}}, \
{('D', 'E'), ('E', 'A'), ('C', 'D'), ('A', 'B'), ('A', 'C'), ('B', 'C')}), True)
    >>> result = find_euler_cycle(({'A': {'B', 'C'},'B': {'A', 'C'},'C': {'A', 'B', 'D', 'E'}, \
'D':{'C', 'E'},'E': {'C', 'D'}},{('A', 'B'), ('B', 'C'), ('C', 'A'),('C', 'D'), ('D', 'E'), \
('E', 'C')}))
    >>> len(result) == 7
    True
    >>> find_euler_cycle(({'A': {'B'},'B': {'C'},'C': {'A', 'D'}, 'D': {'E'},'E': {'C'}},\
{('A', 'B'), ('B', 'C'), ('C', 'A'), ('C', 'D'), ('D', 'E'), ('E', 'C')}), True)
    ['A', 'B', 'C', 'D', 'E', 'C', 'A']
    >>> graph_dir = ({'A': {'B'}, 'B': {'C'}, 'C': {'A'}}, {('A','B'), ('B','C'), ('C','A')})
    >>> find_euler_cycle(graph_dir, True)
    ['A', 'B', 'C', 'A']
    """
    original_connections, edges = graph
    #create a deep copy, because we'll delete some edges and let's save the original dict as it is
    #Adjacency – суміжність
    adj = {node: neighbors.copy() for node, neighbors in original_connections.items()}

    if not edges:
        return None

    all_nodes = list(adj.keys())
    #if there are no nodes
    if not all_nodes:
        return []

    #there are some nodes. is a cycle possible?

    if not oriented:
        #check whether every vertex has an even degree
        for node in adj:
            if len(adj[node]) % 2 != 0:
                return None
        #it is suitable to make a cycle (we will check if the graph is connected at the end)
    else:
        #ins and outsmust be the same (ins-outs = 0)
        balance = {}

        for node, neighbors in adj.items():
            #minus out
            balance[node] = balance.get(node, 0) - len(neighbors)

            for one_neighbor in neighbors:
                #add in
                balance[one_neighbor] = balance.get(one_neighbor, 0) + 1

        #is balance equival zero?
        for node, count in balance.items():
            if count != 0:
                return None

    #start creating the cycle
    start_node = all_nodes[0]
    for node in all_nodes:
        if len(adj[node]) > 0:
            start_node = node
            break

#stack: tracks the current traversal path (allows backtracking)
#circuit: stores the final path (nodes are added when they have no unused edges left)
    stack = [start_node]    #як чернетка
    circuit = []            #як чистовик

#main part of Hierholzer's algorithm
#go forward (deeper) while you can. If can't: save stack[-1] to circuit and go back
    while stack:
        u = stack[-1]
        if u in adj and adj[u]:
            v = adj[u].pop()
            if not oriented:
                if v in adj and u in adj[v]:
                    adj[v].remove(u)
            stack.append(v)
        else:
            circuit.append(stack.pop())

    path = circuit[::-1]

    #now check if the grapg is connected
    total_edges_count = len(edges)
    if oriented:
        total_edges_count = len(edges)
    elif not oriented:
        total_edges_count = len(edges) / 2

    if len(path) - 1 != total_edges_count:
            return None
    return path

if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
