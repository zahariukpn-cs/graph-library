'''Файл з функцією перевірки на ізоморфність'''

def are_isomorphic(graph1: dict, graph2: dict, oriented: bool = False) -> bool:
    '''
    Перевіряє ізоморфність графів
    '''
    if len(graph1) != len(graph2): # перевірка кількості вершин
        return False
    if sum(len(nodes) for nodes in graph1.values()) != \
       sum(len(nodes) for nodes in graph2.values()): # перевірка кількості ребер
        return False

    nodes1 = list(graph1.keys())
    nodes2 = list(graph2.keys())

    # перевірка степенів :_)
    out_degrees1 = {el: len(graph1[el]) for el in nodes1}
    out_degrees2 = {el: len(graph2[el]) for el in nodes2}
    in_degrees1, in_degrees2 = {}, {}

    if oriented:
        def get_in_degrees(graph, nodes):
            # для орієнтованих треба знати, скільки інших вершин посилаються НА вершину
            res = {n: 0 for n in nodes}

            for i in graph:
                for j in graph[i]:
                    if j in res:
                        res[j] += 1
            return res

        in_degrees1 = get_in_degrees(graph1, nodes1)
        in_degrees2 = get_in_degrees(graph2, nodes2)

        if sorted(out_degrees1.values()) != sorted(out_degrees2.values()) or \
           sorted(in_degrees1.values()) != sorted(in_degrees2.values()):
            return False
    else:
        if sorted(out_degrees1.values()) != sorted(out_degrees2.values()):
            return False

    if oriented:
        nodes1.sort(key=lambda x: out_degrees1[x] + in_degrees1[x], reverse=True)
    else:
        nodes1.sort(key=lambda x: out_degrees1[x], reverse=True)

    connectings = {}
    used_nodes_g2 = set()

    # тут перевіряємо, чи можна встановити відповідність між вершинами
    def is_compatible(u, v):
        if out_degrees1[u] != out_degrees2[v]:
            return False
        if oriented and in_degrees1[u] != in_degrees2[v]:
            return False

        # перевірка зв'язків з вже доданими вершинами
        for connected_u, connected_v in connectings.items():
            if (connected_u in graph1[u]) != (connected_v in graph2[v]):
                return False
            # перевірка зворотного зв'язку
            if oriented and (u in graph1[connected_u]) != (v in graph2[connected_v]):
                return False
        return True

    # тут підбираємо пари відповідних вершин з обох графів
    def solve(index):
        # якщо дійшли до кінця списку вершин - значить ізоморфні
        if index == len(nodes1):
            return True

        u = nodes1[index]
        for v in nodes2:
            if v not in used_nodes_g2:
                if is_compatible(u, v):
                    # записуємо пару
                    connectings[u] = v
                    used_nodes_g2.add(v)

                    if solve(index + 1):
                        return True

                    # видаляємо пару, якщо далі не склалася бієкція
                    del connectings[u]
                    used_nodes_g2.remove(v)
        return False

    return solve(0)
