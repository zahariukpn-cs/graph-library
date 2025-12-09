import argparse

from read_graph_from_csv import read_graph_from_csv_to_dict
from read_graph_from_csv import read_graph_from_csv_to_set
from euler_cycle import find_euler_cycle
from graph_painting import is_bipartite, three_coloring
from isomorphism import are_isomorphic
from gamilton import make_way


def main():
    #парсер
    parser = argparse.ArgumentParser(
        description="Бібліотека для роботи з графами.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    #Аргументи
    parser.add_argument('file', type=str, help='Шлях до CSV файлу з графом')
    parser.add_argument('--oriented', action='store_true', help='Прапорець: вважати граф орієнтованим')

    #дії
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument('--show', action='store_true', help='Просто зчитати та вивести граф')
    action_group.add_argument('--euler', action='store_true', help='Знайти Ейлерів цикл')
    action_group.add_argument('--hamilton', action='store_true', help='Знайти Гамільтонів цикл')
    action_group.add_argument('--bipartite', action='store_true', help='Перевірити на дводольність')
    action_group.add_argument('--coloring', action='store_true', help='Виконати 3-розфарбування')
    action_group.add_argument('--isomorph', action='store_true', help='Перевірити ізоморфізм')

    #додатковий файл для ізоморфізму
    parser.add_argument('--file2', type=str, help='Шлях до другого файлу (для ізоморфізму)', default=None)

    args = parser.parse_args()

    #Підготовка даних
    #перетвор bool  у str ('directed'/'undirected') для функцій зчитування
    mode_str = 'directed' if args.oriented else 'undirected'


    #Виконання
    if args.euler:
        #Ейлеру потрібен кортеж (dict, set)
        graph_dict = read_graph_from_csv_to_dict(args.file, mode_str)
        graph_edges = read_graph_from_csv_to_set(args.file, mode_str)

        if graph_dict is None or graph_edges is None:
            return #вихід бо помилка читання

        graph_tuple = (graph_dict, graph_edges)

        #oriented як bool, бо функція Ейлера чекає bool
        result = find_euler_cycle(graph_tuple, oriented=args.oriented)
        print(f"Ейлерів цикл: {result}")

    elif args.hamilton:
        graph_dict = read_graph_from_csv_to_dict(args.file, mode_str)
        if graph_dict is None:
            return
        result = make_way(graph_dict)
        print(f"Гамільтонів цикл: {result}")

    elif args.bipartite:
        # Приймає dict
        graph_dict = read_graph_from_csv_to_dict(args.file, mode_str)
        if graph_dict is None:
            return

        result = is_bipartite(graph_dict)
        print(f"Граф дводольний: {result}")

    elif args.coloring:
        # Приймає dict
        graph_dict = read_graph_from_csv_to_dict(args.file, mode_str)
        if graph_dict is None:
            return

        result = three_coloring(graph_dict)
        print(f"Розфарбування: {result}")

    elif args.isomorph:
        #потребує двох файлів
        if not args.file2:
            print("Помилка: Для ізоморфізму вкажіть другий файл через --file2")
            return

        graph1 = read_graph_from_csv_to_dict(args.file, mode_str)
        graph2 = read_graph_from_csv_to_dict(args.file2, mode_str)

        if graph1 is None or graph2 is None:
            return

        result = are_isomorphic(graph1, graph2)
        print(f"Графи ізоморфні: {result}")

    elif args.show:
        graph_dict = read_graph_from_csv_to_dict(args.file, mode_str)
        if graph_dict is None:
            return
        print(f"Зчитаний граф: {graph_dict}")

if __name__ == "__main__":
    main()
