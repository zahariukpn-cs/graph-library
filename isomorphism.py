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


# # ==========================================
# # ТЕСТОВІ ДАНІ
# # ==========================================

# # --- ТЕСТ 1: Неорієнтовані прості (Ізоморфні) ---
# # Граф: 1-2-3-1 (Трикутник)
# G1_triangle = {
#     1: {2, 3},
#     2: {1, 3},
#     3: {1, 2}
# }
# # Граф: a-b-c-a (Трикутник з буквами)
# G2_triangle = {
#     'a': {'b', 'c'},
#     'b': {'a', 'c'},
#     'c': {'a', 'b'}
# }

# # --- ТЕСТ 2: Неорієнтовані (Різна структура) ---
# # Граф: 1-2-3 (Лінія). Степені: {1:1, 2:2, 3:1}
# G3_line = {
#     1: {2},
#     2: {1, 3},
#     3: {2}
# }
# # (Порівнюємо з трикутником G1, де всі степені 2)

# # --- ТЕСТ 3: Орієнтовані (Напрямок важливий) ---
# # Граф: 1 -> 2 -> 3 -> 1 (Цикл)
# G4_cycle_dir = {
#     1: {2},
#     2: {3},
#     3: {1}
# }
# # Граф: 1 -> 2 <- 3 -> 1 (Злиття в точці 2). Структурно інший.
# G5_conflict_dir = {
#     1: {2},     # 1 посилається на 2
#     2: set(),   # 2 ні на кого не посилається (тупик)
#     3: {1, 2}   # 3 посилається і на 1, і на 2
# }

# # --- ТЕСТ 4: Хитрий випадок (Однакові степені, різна топологія) ---
# # Шестикутник (1 цикл на 6 вершин). Всі вершини мають степінь 2.
# G6_hexagon = {
#     1: {2, 6}, 2: {1, 3}, 3: {2, 4},
#     4: {3, 5}, 5: {4, 6}, 6: {5, 1}
# }
# # Два окремих трикутники (2 цикли по 3 вершини). Теж 6 вершин, всі степінь 2.
# G7_two_triangles = {
#     'a': {'b', 'c'}, 'b': {'a', 'c'}, 'c': {'a', 'b'},
#     'd': {'e', 'f'}, 'e': {'d', 'f'}, 'f': {'d', 'e'}
# }

# # ==========================================
# # ЗАПУСК ТЕСТІВ
# # ==========================================

# def run_test(name, g1, g2, directed, expected):
#     result = are_isomorphic(g1, g2, directed)
#     status = "✅ OK" if result == expected else "❌ FAIL"
#     print(f"[{status}] {name}: Очікувалось {expected}, отримано {result}")

# print("\n--- Запуск тестів ---")

# # 1. Трикутник vs Трикутник (Неорієнтований)
# run_test("Трикутник (ізоморфні)", G1_triangle, G2_triangle, False, True)

# # 2. Трикутник vs Лінія (Неорієнтований)
# run_test("Трикутник vs Лінія (різні)", G1_triangle, G3_line, False, False)

# # 3. Орієнтований цикл vs Орієнтований цикл (Ізоморфні)
# # Створимо копію циклу, але з іншими ID, щоб перевірити True
# G4_copy = {'x': {'y'}, 'y': {'z'}, 'z': {'x'}}
# run_test("Орієнтовані цикли (ізоморфні)", G4_cycle_dir, G4_copy, True, True)

# # 4. Орієнтований цикл vs Конфлікт (Різні)
# run_test("Цикл vs Злиття (різні)", G4_cycle_dir, G5_conflict_dir, True, False)

# # 5. Шестикутник vs 2 Трикутники (Складний випадок)
# # Якщо функція перевіряє тільки степені, вона скаже True (помилка).
# # Якщо працює перевірка зв'язків (BFS/DFS або наш Backtracking), вона скаже False (правильно).
# run_test("Hexagon vs 2 Triangles (різні)", G6_hexagon, G7_two_triangles, False, False)
