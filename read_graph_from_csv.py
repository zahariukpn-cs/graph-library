def read_graph_from_csv_to_dict(filename:str, oriented:bool=False)\
      -> dict[str, set[str]]:
    """
    Reads a graph from a CSV file (NodeA,NodeB per line)\
          into an adjacency list and an edge set.

    Args:
        filename (str): Path to the CSV file. Each line\
              must be 'NodeA,NodeB'.
        oriented (bool, optional): If True, the graph is\
              directed. Defaults to False (undirected).

    Returns:
        tuple[dict[str, set[str]], set[tuple[str, str]]]:
            (adjacency_dict, edge_set)
            - Adjacency dict (connections): Keys are nodes,\
                  values are sets of neighbors.
            - Edge set (edges): All (source, destination)\
                  tuples.
    """

    connections = {}

    with open(filename, 'r', encoding='utf-8') as file:
        file = file.readlines()

    for line in file:

        # Nodes are written by comma
        line = line.strip().split(',')
        length = len(line)

        # There are no more than 2 nodes in each line
        if length > 2 or length < 2:
            continue
        note1, note2 = line[0], line[-1]
        if note1 in connections:
            connections[note1] |= {note2}
        else:
            connections |= {note1: {note2}}
        if not oriented:
            if note2 in connections:
                connections[note2] |= {note1}
            else:
                connections |= {note2: {note1}}

    return connections

def read_graph_from_csv_to_set(filename:str, oriented:bool=False)\
      -> set[tuple[str, str]]:
    """
    Reads a graph from a CSV file (NodeA,NodeB per line)\
          into an adjacency list and an edge set.

    Args:
        filename (str): Path to the CSV file. Each line\
              must be 'NodeA,NodeB'.
        oriented (bool, optional): If True, the graph is\
              directed. Defaults to False (undirected).

    Returns:
        tuple[dict[str, set[str]], set[tuple[str, str]]]:
            (adjacency_dict, edge_set)
            - Adjacency dict (connections): Keys are nodes,\
                  values are sets of neighbors.
            - Edge set (edges): All (source, destination)\
                  tuples.
    """

    edges = set()

    with open(filename, 'r', encoding='utf-8') as file:
        file = file.readlines()

    for line in file:

        # Nodes are written by comma
        line = line.strip().split(',')
        length = len(line)

        # There are no more than 2 nodes in each line
        if length > 2 or length < 2:
            continue
        note1, note2 = line[0], line[-1]
        edges |= {(note1, note2)}
        if not oriented:
            edges |= {(note2, note1)}

    return edges
