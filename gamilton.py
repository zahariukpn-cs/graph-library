"""Gamilton's Scicle"""
import time


def make_way(graph: dict, passed_way = None)-> list|bool:
    """
    This function help to make gamiltons way by list of tops.
    If this function has this way, than it return way.
    If not returns False.



    >>> graph = {1: {2, 3}, 2: {4, 5}, 3: {2, 4}, 4: {1, 5}, 5: {2, 4}}
    >>> make_way(graph)
    [1, 3, 2, 5, 4, 1]

    >>> graph6 = {1: {2, 3}, 2: {1, 4, 5}, 3: {1, 4, 6}, 4: {2, 3, 5}, 5: {2, 4, 6}, 6: {3, 5}}
    >>> make_way(graph6)
    [1, 2, 4, 5, 6, 3, 1]

    >>> graph7 = {1: {2, 7}, 2: {1, 3}, 3: {2, 4}, 4: {3, 5}, 5: {4, 6}, 6: {5, 7}, 7: {6, 1}}
    >>> make_way(graph7)
    [1, 2, 3, 4, 5, 6, 7, 1]

    >>> graph6_branch = {1: {2}, 2: {1, 3, 5}, 3:{2, 4}, 4: {3, 6}, 5: {2, 6}, 6: {4, 5}}
    >>> make_way(graph6_branch)
    False

    >>> undirected_tree = {
    ... 1: {2},
    ... 2: {1, 3},
    ... 3: {2, 4},
    ... 4: {3}
    ... }
    >>> make_way(undirected_tree)
    False

    >>> directed_dense = {
    ... 1: {2, 3},
    ... 2: {3, 4},
    ... 3: {4, 1},
    ... 4: {1, 2}
    ... }
    >>> make_way(directed_dense)
    [1, 2, 3, 4, 1]

    >>> directed_loop = {
    ... 1: {1, 2},
    ... 2: {3},
    ... 3: {1}
    ... }
    >>> make_way(directed_loop)
    [1, 2, 3, 1]

    >>> undirected_loop = {
    ... 1: {1, 2},
    ... 2: {1, 3},
    ... 3: {2}
    ... }
    >>> make_way(undirected_loop)
    False

    >>> graph20 = {
    ... 1: {2, 20}, 2: {1, 3}, 3: {2, 4}, 4: {3, 5}, 5: {4, 6},
    ... 6: {5, 7}, 7: {6, 8}, 8: {7, 9}, 9: {8, 10}, 10: {9, 11},
    ... 11: {10, 12}, 12: {11, 13}, 13: {12, 14}, 14: {13, 15}, 15: {14, 16},
    ... 16: {15, 17}, 17: {16, 18}, 18: {17, 19}, 19: {18, 20}, 20: {19, 1}
    ... }
    >>> make_way(graph20)
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 1]

    >>> single_node = {1: {1}}
    >>> make_way(single_node)
    False

    >>> isolated = {
    ... 1: {2},
    ... 2: {1},
    ... 3: set()
    ... }
    >>> make_way(isolated)
    False

    >>> undirected_loop = {
    ... '1': {'2', '3', '4', '5', '6'},
    ... '2': {'1'},
    ... '3': {'1'},
    ... '4': {'1'},
    ... '5': {'1'},
    ... '6': {'1'}
    ... }
    >>> make_way(undirected_loop)
    False

    >>> bad_graph = {1: {2}, 2: {1, 3}, 3: {2, 4}, 4: {3}}
    >>> make_way(bad_graph)
    False
    """
    if len(graph)<=2:
        return False
    if not passed_way:
        for first_top in graph:     # Підбір початкової точки циклу
            passed_way = [first_top]
            res = make_way(graph, passed_way)
            if res:
                return res
            passed_way = []                    # Повернення результату
        return False    # У випадку перебору всіх варіантів і не знаходження правильного.

    if passed_way:
        if len(passed_way) == len(graph) and passed_way[0] in graph[passed_way[-1]]:
            return passed_way + [passed_way[0]]
    for top in graph[passed_way[-1]]: # Перебір наступних можливих точок
        if top not in passed_way:
            passed_way.append(top) #Якщо вони не пройдені, тоді вони додаються
            res = make_way(graph, passed_way)
            if res:
                return res
            passed_way.pop() # У випадку тупіка видаляємо останій елемент
    return False # Якщо нам не підходить ні один варіант, тобто тупік

def generate_graph_n(n):
    """
    This function generate graphs for analise
    """
    graph = {}
    for i in range(1, n+1):
        neigh = set()
        # циклічні сусіди
        neigh.add(i-1 if i > 1 else n)   # попередній (для 1 -> 1000)
        neigh.add(i+1 if i < n else 1)   # наступний (для 1000 -> 1)
        # хорда вперед (i, i+2) якщо існує
        if i <= n-2:
            neigh.add(i+2)
        # хорда назад (i-2, i) якщо існує (створює симетрію для хорд)
        if i >= 3:
            neigh.add(i-2)
        # зберігаємо відсортований список для детермінованості
        graph[i] = sorted(neigh)
    return graph

def time_for_n(n):
    """
    This function return time if working for another function.
    """
    graph = generate_graph_n(n)
    start_time = time.time()
    make_way(graph)
    end_time = time.time()
    fial_time = abs(start_time - end_time)
    return fial_time

def analise():
    """
    This function help to analise how this way of building gamilron's cycle
    is effective for different graphs from 100 to 950 tops.
    """
    for i in range(100, 1000, 50):
        print(f"Час роботи з графом у якого {i} вершин: {time_for_n(i)}")

analise()

if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
