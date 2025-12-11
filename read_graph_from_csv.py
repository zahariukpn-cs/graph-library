def read_graph_from_csv_to_dict(filename:str, oriented:str='undirected')\
      -> dict[str, set[str]]:
    """
    Reads a graph from a CSV file (NodeA,NodeB per line)\
          into an adjacency list and an edge set.

    Args:
        filename (str): Path to the CSV file. Each line\
              must be 'NodeA,NodeB'.
        oriented (str, optional): If 'directed', the graph is\
              directed. Defaults to 'undirected' (undirected).

    Returns:
        dict[str, set[str]]:
            - Adjacency dict (connections): Keys are nodes,\
                  values are sets of neighbors.
    """

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            file = file.readlines()
    except FileNotFoundError:
        return 'Не існує файлу з такою назвою в поточній директорії.'

    connections = {}

    for line in file:

        # Nodes are written by comma
        line = line.strip().split(',')
        length = len(line)

        # There are no more than 2 nodes in each line
        if length != 2 or line[-1] == '':
            raise ValueError('Програма зчитує лише один граф')
        note1, note2 = line[0], line[-1]
        if note1 in connections:
            connections[note1] |= {note2}
        else:
            connections |= {note1: {note2}}
        if oriented == 'undirected':
            if note2 in connections:
                connections[note2] |= {note1}
            else:
                connections |= {note2: {note1}}
        elif oriented != 'directed':
            return 'Вкажіть "directed" у полі вводу, якщо граф орієнтований'

    return connections

def read_graph_from_csv_to_set(filename:str, oriented:str='undirected')\
      -> set[tuple[str, str]]:
    """
    Reads a graph from a CSV file (NodeA,NodeB per line)\
          into an adjacency list and an edge set.

    Args:
        filename (str): Path to the CSV file. Each line\
              must be 'NodeA,NodeB'.
        oriented (str, optional): If 'directed', the graph is\
              directed. Defaults to 'undirected' (undirected).

    Returns:
        set[tuple[str, str]]:
            - Edge set (edges): All (source, destination)\
                  tuples.
    """

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            file = file.readlines()
    except FileNotFoundError:
        print('Не існує файлу з такою назвою в поточній директорії.')

    edges = set()

    for line in file:

        # Nodes are written by comma
        line = line.strip().split(',')
        length = len(line)

        # There are no more than 2 nodes in each line
        if length != 2 or line[-1] == '':
            raise ValueError('Програма зчитує лише один граф')
        note1, note2 = line[0], line[-1]
        edges |= {(note1, note2)}
        if oriented == 'undirected':
            edges |= {(note2, note1)}
        elif oriented != 'directed':
            return 'Вкажіть "directed" у полі вводу, якщо граф орієнтований'

    return edges
