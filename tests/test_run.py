import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from algorithms.read_graph_from_csv import read_graph_from_csv_to_dict

FILE_PATH = 'tests/data/graph.csv' 

try:
    graph = read_graph_from_csv_to_dict(FILE_PATH, oriented='undirected')

    print("Результат:")
    print(graph)
    
except ValueError as e:
    print(f"Помилка формату файлу: {e}")
except FileNotFoundError:
    print(f"Помилка: Файл {FILE_PATH} не знайдено.")
