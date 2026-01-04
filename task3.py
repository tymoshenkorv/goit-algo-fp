"""
Завдання 3. Алгоритм Дейкстри з бінарною купою

Реалізація алгоритму Дейкстри для знаходження найкоротших шляхів
уcі з використанням бінарної купи (heap) для оптимізації.
"""

import heapq
from typing import Dict, List, Tuple, Optional


class WeightedGraph:
    """Зважений граф представлений списком суміжності"""

    def __init__(self):
        self.graph: Dict[str, List[Tuple[str, int]]] = {}

    def add_vertex(self, vertex: str):
        """Додає вершину до графа"""
        if vertex not in self.graph:
            self.graph[vertex] = []

    def add_edge(self, from_vertex: str, to_vertex: str, weight: int):
        """Додає зважене ребро до графа"""
        # Додаємо вершини, якщо їх немає
        self.add_vertex(from_vertex)
        self.add_vertex(to_vertex)

        # Додаємо ребро (для неорієнтованого графа додаємо в обидві сторони)
        self.graph[from_vertex].append((to_vertex, weight))
        self.graph[to_vertex].append((from_vertex, weight))

    def get_vertices(self) -> List[str]:
        """Повертає список всіх вершин"""
        return list(self.graph.keys())

    def get_neighbors(self, vertex: str) -> List[Tuple[str, int]]:
        """Повертає список сусідів вершини з вагами ребер"""
        return self.graph.get(vertex, [])

    def __str__(self):
        """Строкове представлення графа"""
        result = "Граф:\n"
        for vertex in sorted(self.graph.keys()):
            neighbors = ", ".join([f"{n}({w})" for n, w in self.graph[vertex]])
            result += f"{vertex}: {neighbors}\n"
        return result


def dijkstra(
    graph: WeightedGraph, start_vertex: str
) -> Tuple[Dict[str, float], Dict[str, Optional[str]]]:
    """
    Алгоритм Дейкстри з використанням бінарної купи.

    Args:
        graph: Зважений граф
        start_vertex: Початкова вершина

    Returns:
        Tuple з двох словників:
        - distances: відстані від початкової вершини до всіх інших
        - previous: попередні вершини в найкоротших шляхах
    """

    # Ініціалізація відстаней (нескінченність для всіх, крім стартової)
    distances = {vertex: float("infinity") for vertex in graph.get_vertices()}
    distances[start_vertex] = 0

    # Словник для відстеження попередніх вершин (для відновлення шляху)
    previous = {vertex: None for vertex in graph.get_vertices()}

    # Бінарна купа (min-heap) для ефективного вибору вершини з мінімальною відстанню
    # Формат: (відстань, вершина)
    priority_queue = [(0, start_vertex)]

    # Множина відвіданих вершин
    visited = set()

    while priority_queue:
        # Витягуємо вершину з найменшою відстанню
        current_distance, current_vertex = heapq.heappop(priority_queue)

        # Якщо вершина вже відвідана, пропускаємо
        if current_vertex in visited:
            continue

        # Позначаємо вершину як відвідану
        visited.add(current_vertex)

        # Якщо знайдена відстань більша за збережену, пропускаємо
        # (може статися через дублікати в купі)
        if current_distance > distances[current_vertex]:
            continue

        # Переглядаємо всіх сусідів поточної вершини
        for neighbor, weight in graph.get_neighbors(current_vertex):
            # Обчислюємо нову відстань через поточну вершину
            distance = current_distance + weight

            # Якщо знайшли коротший шлях, оновлюємо
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_vertex
                # Додаємо в купу з новою відстанню
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances, previous


def reconstruct_path(
    previous: Dict[str, Optional[str]], start_vertex: str, end_vertex: str
) -> List[str]:
    """
    Відновлює найкоротший шлях від початкової до кінцевої вершини.

    Args:
        previous: Словник попередніх вершин
        start_vertex: Початкова вершина
        end_vertex: Кінцева вершина

    Returns:
        Список вершин у найкоротшому шляху
    """
    path = []
    current = end_vertex

    # Якщо немає шляху до кінцевої вершини
    if previous[current] is None and current != start_vertex:
        return []

    # Відновлюємо шлях у зворотному порядку
    while current is not None:
        path.append(current)
        current = previous[current]

    # Повертаємо шлях у правильному порядку
    path.reverse()
    return path


def print_shortest_paths(graph: WeightedGraph, start_vertex: str):
    """
    Виводить найкоротші шляхи від початкової вершини до всіх інших.

    Args:
        graph: Зважений граф
        start_vertex: Початкова вершина
    """
    print(f"\n{'=' * 70}")
    print(f"Найкоротші шляхи від вершини '{start_vertex}'")
    print(f"{'=' * 70}\n")

    # Виконуємо алгоритм Дейкстри
    distances, previous = dijkstra(graph, start_vertex)

    # Виводимо результати для кожної вершини
    for vertex in sorted(graph.get_vertices()):
        if vertex == start_vertex:
            print(f"Вершина {vertex}: відстань = 0 (початкова вершина)")
        else:
            distance = distances[vertex]
            if distance == float("infinity"):
                print(f"Вершина {vertex}: недосяжна")
            else:
                path = reconstruct_path(previous, start_vertex, vertex)
                path_str = " → ".join(path)
                print(f"Вершина {vertex}: відстань = {distance}, шлях: {path_str}")

    print(f"\n{'=' * 70}\n")


def create_example_graph1() -> WeightedGraph:
    """Створює приклад графа для демонстрації"""
    graph = WeightedGraph()

    # Додаємо ребра (граф автоматично створює вершини)
    graph.add_edge("A", "B", 4)
    graph.add_edge("A", "C", 2)
    graph.add_edge("B", "C", 1)
    graph.add_edge("B", "D", 5)
    graph.add_edge("C", "D", 8)
    graph.add_edge("C", "E", 10)
    graph.add_edge("D", "E", 2)
    graph.add_edge("D", "F", 6)
    graph.add_edge("E", "F", 3)

    return graph


def demonstrate_algorithm_steps(graph: WeightedGraph, start_vertex: str):
    """
    Демонструє покрокову роботу алгоритму Дейкстри.

    Args:
        graph: Зважений граф
        start_vertex: Початкова вершина
    """
    print(f"\n{'=' * 70}")
    print("Покрокова демонстрація алгоритму Дейкстри")
    print(f"Початкова вершина: {start_vertex}")
    print(f"{'=' * 70}\n")

    # Ініціалізація
    distances = {vertex: float("infinity") for vertex in graph.get_vertices()}
    distances[start_vertex] = 0
    previous = {vertex: None for vertex in graph.get_vertices()}
    priority_queue = [(0, start_vertex)]
    visited = set()
    step = 0

    print("Крок 0: Ініціалізація")
    print(f"Відстані: {start_vertex}=0, інші=∞")
    print(f"Купа: [(0, '{start_vertex}')]")
    print()

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        if current_vertex in visited:
            continue

        step += 1
        visited.add(current_vertex)

        print(
            f"Крок {step}: Обробка вершини '{current_vertex}' (відстань={current_distance})"
        )

        if current_distance > distances[current_vertex]:
            continue

        updates = []
        for neighbor, weight in graph.get_neighbors(current_vertex):
            distance = current_distance + weight

            if distance < distances[neighbor]:
                old_dist = distances[neighbor]
                distances[neighbor] = distance
                previous[neighbor] = current_vertex
                heapq.heappush(priority_queue, (distance, neighbor))
                updates.append(
                    f"  {neighbor}: {old_dist if old_dist != float('infinity') else '∞'} → {distance}"
                )

        if updates:
            print("Оновлення відстаней:")
            for update in updates:
                print(update)
        else:
            print("  Немає оновлень")

        print(f"Відвідано: {sorted(visited)}")
        print()

    print(f"{'=' * 70}\n")


if __name__ == "__main__":
    # Приклад 1: Простий граф з літерами
    print("\n" + "=" * 70)
    print("ПРИКЛАД 1: Простий граф")
    print("=" * 70)

    graph1 = create_example_graph1()
    print(graph1)

    print_shortest_paths(graph1, "A")

    # Покрокова демонстрація на простому графі
    demonstrate_algorithm_steps(graph1, "A")
