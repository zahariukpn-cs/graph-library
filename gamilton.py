"""Gamilton's Scicle"""


def make_way(graph: dict, passed_way = None, passed_first_el = None)-> list|bool:
    """
    This function help to make gamiltons way by list of tops.
    If this function has this way, than it return way.
    If not returns False.
    >>> graph = {1: [2, 3], 2: [4, 5], 3:[2, 4], 4: [1, 5], 5: [2, 4]}
    >>> make_way(graph)
    [1, 3, 2, 5, 4, 1]
    >>> graph6 = {1: [2, 3], 2: [1, 4, 5], 3: [1, 4, 6], 4: [2, 3, 5], 5: [2, 4, 6], 6: [3, 5]}
    >>> make_way(graph6)
    [1, 2, 4, 5, 6, 3, 1]
    >>> graph7 = {1: [2, 7], 2: [1, 3], 3: [2, 4], 4: [3, 5], 5: [4, 6], 6: [5, 7], 7: [6, 1]}
    >>> make_way(graph7)
    [1, 2, 3, 4, 5, 6, 7, 1]
    >>> graph6_branch = {1: [2], 2: [1, 3, 5], 3: [2, 4], 4: [3, 6], 5: [2, 6], 6: [4, 5]}
    >>> make_way(graph6_branch)
    False
    >>> graph20 = {
    ... 1: [2, 20], 2: [1, 3], 3: [2, 4], 4: [3, 5], 5: [4, 6],
    ... 6: [5, 7], 7: [6, 8], 8: [7, 9], 9: [8, 10], 10: [9, 11],
    ... 11: [10, 12], 12: [11, 13], 13: [12, 14], 14: [13, 15], 15: [14, 16],
    ... 16: [15, 17], 17: [16, 18], 18: [17, 19], 19: [18, 20], 20: [19, 1]
    ... }
    >>> make_way(graph20)
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 1]
    >>> bad_graph = {1: [2], 2: [1, 3], 3: [2, 4], 4: [3]}
    >>> make_way(bad_graph)
    False
    """
    if not passed_first_el:
        passed_first_el = []
    if not passed_way:
        passed_way = []
        for first_top in graph:
            if first_top not in passed_first_el:
                passed_first_el.append(first_top)
                passed_way.append(first_top)
                res = make_way(graph, passed_way, passed_first_el)
                if res:
                    return res
        return False

    if passed_way:
        if len(passed_way) == len(graph) and passed_way[0] in graph[passed_way[-1]]:
            return passed_way + [passed_way[0]]
    for top in graph[passed_way[-1]]:
        if top not in passed_way:
            passed_way.append(top)
            res = make_way(graph, passed_way, passed_first_el)
            if res:
                return res
            passed_way.pop()
    return False



if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
