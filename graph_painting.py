def is_bipartite(ghraph: dict) -> bool:
    """
     Checks whether an undirected graph is bipartite.

    A graph is bipartite if its vertices can be divided into two groups
    such that no two adjacent vertices belong to the same group.
    This function uses BFS coloring to verify this property.

    Args:
        graph (dict): A dictionary representing the graph.
                      Keys are node names, and values are lists of adjacent nodes.

    Returns:
        bool: True if the graph is bipartite, False otherwise.

    Examples:
        >>> g1 = {
        ...     'A': ['B'],
        ...     'B': ['A', 'C'],
        ...     'C': ['B']
        ... }
        >>> is_bipartite(g1)
        True

        >>> g2 = {
        ...     'A': ['B', 'C'],
        ...     'B': ['A', 'C'],
        ...     'C': ['A', 'B']
        ... }
        >>> is_bipartite(g2)
        False

        >>> g3 = {
        ...     '1': ['2'],
        ...     '2': ['1'],
        ...     '3': []  # isolated node
        ... }
        >>> is_bipartite(g3)
        True
    """
    color = {}
    queue = []
    #BFS
    for node in ghraph:
        if node not in color:
            queue = [node]
            color[node] = 'A'

            while queue:
                current_node = queue.pop(0)
                for adjacent in ghraph.get(current_node, []):
                    if adjacent not in color:
                        if color[current_node] == 'A':
                            color[adjacent] = 'B'
                        elif color[current_node] == 'B':
                            color[adjacent] = 'A'
                        queue.append(adjacent)
                    else:
                        if color[current_node] == color[adjacent]:
                            return False
    return True

def three_coloring(graph: dict) -> dict:
    """
    Attempts to color the nodes of an undirected graph using three colors: A, B, and C.

    The function uses depth-first search with backtracking to assign a color to each node
    such that no two adjacent nodes share the same color.

    Args:
        graph (dict):
            A dictionary representing the graph.
            Keys are node names (strings), and values are lists of adjacent nodes.

    Returns:
        dict:
            A dictionary where each node is assigned one of the colors 'A', 'B', or 'C'.
            If the graph cannot be colored with three colors, returns the string
            'Impossible to paint'.

    Examples:
        >>> graph1 = {
        ...     'A': ['B', 'C'],
        ...     'B': ['A', 'C'],
        ...     'C': ['A', 'B']
        ... }
        >>> result1 = three_coloring(graph1)
        >>> set(result1.values()) <= {'A', 'B', 'C'}
        True

        >>> graph2 = {
        ...     'X': ['Y'],
        ...     'Y': ['X', 'Z'],
        ...     'Z': ['Y']
        ... }
        >>> result2 = three_coloring(graph2)
        >>> isinstance(result2, dict)
        True
        >>> all(color in 'ABC' for color in result2.values())
        True

        >>> graph3 = {'A': []}  # single isolated node
        >>> three_coloring(graph3)
        {'A': 'A'}
    """
    color = {item: None for item in graph} #all aren`t painted
    nodes = list(graph.keys())

    def is_to_paint(node_to_paint, color_to_try): #checking if we can color node
        for item in graph.get(node_to_paint, []):
            if color.get(item) == color_to_try:
                return False
        return True

    def paint(node_index):
        #DFS
        if node_index == len(color): #found a complete and valid coloring of the graph
            return True
        node_to_paint = nodes[node_index]
        for color_to_try in 'ABC':
            if is_to_paint(node_to_paint, color_to_try):
                color[node_to_paint] = color_to_try
                if paint(node_index + 1): #checking for next node
                    return True
                #next interation try another color
                color[node_to_paint] = None #if we are in situation when we can`t paint any of colors`
        return False #no color matched

    if paint(0): #start painting with first node
        return color
    return 'Impossible to paint'

if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
