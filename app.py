import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

from euler_cycle import find_euler_cycle
from gamilton import make_way
from graph_painting import is_bipartite, three_coloring
from isomorphism import are_isomorphic

# Зчитування графу
def parse_graph_input(text_input: str, oriented: bool):
    """
    Парсить текст у форматі CSV (NodeA,NodeB).
    Повертає: (connections: dict, edges: set, error: str)
    """
    lines = text_input.strip().split('\n')
    if not text_input.strip():
        return None, None, "Введіть дані графу або завантажте файл."

    connections = {}
    edges = set()

    for i, line in enumerate(lines, 1):
        parts = line.strip().split(',')
        length = len(parts)

        # Перевірка на кількість вузлів
        if length != 2:
            return None, None, f"Row {i}: Програма зчитує лише одне ребро (має бути 2 вузли)"

        node1, node2 = parts[0].strip(), parts[1].strip()

        if node1 in connections:
            connections[node1].add(node2)
        else:
            connections[node1] = {node2}

        edges.add((node1, node2))

        if not oriented:
            if node2 in connections:
                connections[node2].add(node1)
            else:
                connections[node2] = {node1}
            edges.add((node2, node1))

    # у NetworkX усі вузли мають бути ключами в dict
    for u, v in list(edges):
        if v not in connections:
            connections[v] = set()
        if u not in connections:
            connections[u] = set()

    return connections, edges, None

# Візуалізація графу
def draw_graph(graph_dict, oriented, path_edges=None, node_colors=None):
    '''Малюємо граф'''
    g = nx.DiGraph(graph_dict) if oriented else nx.Graph(graph_dict)

    pos = nx.spring_layout(g, seed=42)
    fig, ax = plt.subplots(figsize=(6, 4))

    # Кольори вузлів
    colors = [node_colors.get(n, '#A0CBE2') for n in g.nodes()] if node_colors else '#A0CBE2'

    # Малюємо основу
    nx.draw(g, pos, ax=ax, with_labels=True, node_color=colors,
            edge_color='gray', node_size=500, font_size=10, arrows=oriented)

    # Якщо треба підсвітити шлях (Ейлерів/Гамільтоновий)
    if path_edges:
        nx.draw_networkx_edges(g, pos, ax=ax, edgelist=path_edges,
                               edge_color='red', width=2, arrows=oriented)

    st.pyplot(fig)

# Інтерфейс
st.set_page_config(page_title="Graph Library Project", layout="wide")
st.title("Бібліотека для роботи з графами")

# Сайдбар
st.sidebar.header("Налаштування роботи")
algo = st.sidebar.radio("Алгоритм", ["Перегляд", "Ейлеровий цикл", "Гамільтоновий цикл", "Дводольність", "3-фарбування", "Ізоморфізм"])
is_oriented = st.sidebar.checkbox("Орієнтований", value=False)
input_txt = st.sidebar.text_area("Ребро (A,B)", value="1,2\n2,3\n3,1", height=150)

# Друге вікно тільки для ізоморфізму
input_txt_2 = ''
if algo == "Ізоморфізм":
    input_txt_2 = st.sidebar.text_area("Дані другого графа", value="a,b\nb,c\nc,a", height=150)

# Основна частина
col1, col2 = st.columns([2, 1])

# Парсинг основного графа
g_dict, g_edges, error = parse_graph_input(input_txt, is_oriented)

if error:
    st.error(error)
elif g_dict:
    # Вивід результатів у праву колонку, графіка - у ліву
    with col2:
        st.subheader("Результат")

        if algo == "Перегляд":
            st.info("Візуалізація графу")
            with col1:
                draw_graph(g_dict, is_oriented)

        elif algo == "Ейлеровий цикл":
            res = find_euler_cycle((g_dict, g_edges), oriented=is_oriented)
            if res:
                st.success(f"Цикл: {res}")
                path = [(res[i], res[i+1]) for i in range(len(res)-1)]
                with col1:
                    draw_graph(g_dict, is_oriented, path_edges=path)
            else:
                st.warning("Ейлеровий цикл неможливий")
                with col1:
                    draw_graph(g_dict, is_oriented)

        elif algo == "Гамільтоновий цикл":
            res = make_way(g_dict)
            if res:
                st.success(f"Цикл: {res}")
                path = [(res[i], res[i+1]) for i in range(len(res)-1)]
                with col1:
                    draw_graph(g_dict, is_oriented, path_edges=path)
            else:
                st.warning("Гамільтоновий цикл не знайдено")
                with col1:
                    draw_graph(g_dict, is_oriented)

        elif algo == "Дводольність":
            res = is_bipartite(g_dict)
            if res:
                st.success("Граф дводольний")
            else:
                st.error("Граф НЕ дводольний")
            with col1:
                draw_graph(g_dict, is_oriented)

        elif algo == "3-фарбування":
            res = three_coloring(g_dict)
            if isinstance(res, list):
                st.success("Розфарбовано!")
                color_map = {n: {'r':'#ff9999','g':'#99ff99','b':'#9999ff'}.get(c,'gray') for n, c in res}
                with col1:
                    draw_graph(g_dict, is_oriented, node_colors=color_map)
            else:
                st.error(res)
                with col1:
                    draw_graph(g_dict, is_oriented)

        elif algo == "Ізоморфізм":
            g_dict_2, _, error_2 = parse_graph_input(input_txt_2, is_oriented)
            if error_2:
                st.error(f"Граф 2: {error_2}")
            elif g_dict_2:
                res = are_isomorphic(g_dict, g_dict_2)
                st.write(f"Ізоморфні: **{res}**")
                with col1:
                    st.write("Граф 1")
                    draw_graph(g_dict, is_oriented)
                    st.write("Граф 2")
                    draw_graph(g_dict_2, is_oriented)
