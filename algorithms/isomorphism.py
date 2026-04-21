'''isomorphism'''
import hashlib

def are_isomorphic(graph1: dict, graph2: dict) -> bool:
    '''
    Determines if two directed graphs are isomorphic using the Weisfeiler-Lehman (1-WL) test.

    This function first performs fast-fail checks (e.g., node count comparison).
    If they pass, it computes canonical structural hashes for both graphs by
    aggregating both incoming and outgoing neighbor information to handle edge direction correctly.

    Args:
        graph1: dict of the first graph
            (keys are nodes, values are sets of outgoing neighbors).
        graph2: dict of the second graph.

    Returns:
        bool: True if the graphs are likely isomorphic (structurally identical), False otherwise.

    Examples:
        >>> G_A = {'a': ['b'], 'b': []}
        >>> G_B = {1: [2], 2: []}
        >>> are_isomorphic(G_A, G_B)
        True

        >>> G_Chain = {0: [1], 1: [2], 2: []}
        >>> G_Collision = {0: [1], 1: [], 2: [1]}
        >>> are_isomorphic(G_Chain, G_Collision)
        False

        >>> are_isomorphic({0: []}, {0: [], 1: []})
        False

        >>> G_Tri1 = {0: [1], 1: [2], 2: [0]}
        >>> G_Tri2 = {10: [20], 20: [30], 30: [10]}
        >>> are_isomorphic(G_Tri1, G_Tri2)
        True
    '''
    if len(graph1) != len(graph2): # check number of nodes
        return False

    def hash_wl(graph: dict) -> list:
        '''
        Computes the canonical sorted hash list for a single graph.
        '''
        incoming = {node: [] for node in graph}

        for key, values in graph.items():
            for value in values:
                if value in incoming:
                    incoming[value].append(key)

        colors = {node: str(len(graph[node])) for node in graph}

        for _ in range(3):
            new_colors = {}

            for node in graph:
                out_colors = sorted([colors[n] for n in graph[node]])
                in_colors = sorted([colors[n] for n in incoming[node]])

                nickname = colors[node] + ''.join(in_colors) + ''.join(out_colors)
                new_colors[node] = hashlib.sha256(nickname.encode()).hexdigest()

            colors = new_colors

        return sorted(colors.values())

    h1 = hash_wl(graph1)
    h2 = hash_wl(graph2)
    return h1 == h2


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
