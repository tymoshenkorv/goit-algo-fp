# Завдання 5. Візуалізація обходу бінарного дерева
# Використовуючи код із завдання 4 для побудови бінарного дерева, необхідно створити програму на Python,
# яка візуалізує обходи дерева: у глибину та в ширину.

# Вона повинна відображати кожен крок у вузлах з різними кольорами, використовуючи 16-систему RGB (приклад #1296F0).
# Кольори вузлів мають змінюватися від темних до світлих відтінків, залежно від послідовності обходу.
# Кожен вузол при його відвідуванні має отримувати унікальний колір, який візуально відображає порядок обходу.
# 👉🏻 Примітка. Використовуйте стек та чергу, НЕ рекурсію

import uuid

import networkx as nx
import matplotlib.pyplot as plt
from collections import deque


class Node:
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color  # Додатковий аргумент для зберігання кольору вузла
        self.id = str(uuid.uuid4())  # Унікальний ідентифікатор для кожного вузла


def add_edges(graph, node, pos, x=0, y=0, layer=1):
    if node is not None:
        graph.add_node(
            node.id, color=node.color, label=node.val
        )  # Використання id та збереження значення вузла
        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2**layer
            pos[node.left.id] = (l, y - 1)
            l = add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
    if node.right:
        graph.add_edge(node.id, node.right.id)
        r = x + 1 / 2**layer
        pos[node.right.id] = (r, y - 1)
        r = add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    return graph


def draw_tree(tree_root):
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    tree = add_edges(tree, tree_root, pos)

    colors = [node[1]["color"] for node in tree.nodes(data=True)]
    labels = {
        node[0]: node[1]["label"] for node in tree.nodes(data=True)
    }  # Використовуйте значення вузла для міток

    plt.figure(figsize=(8, 5))
    nx.draw(
        tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors
    )
    plt.show()


def generate_color_gradient(n):
    """
    Генерує градієнт кольорів від темного до світлого відтінку.

    Args:
        n: Кількість кольорів для генерації

    Returns:
        list: Список кольорів у форматі HEX (#RRGGBB)
    """
    colors = []
    for i in range(n):
        # Від темного (30) до світлого (220) синього відтінку
        intensity = int(30 + (190 * i / (n - 1)) if n > 1 else 30)
        # Градієнт від темно-синього до блакитного
        r = int(intensity * 0.3)  # Червоний компонент
        g = int(intensity * 0.5)  # Зелений компонент
        b = intensity  # Синій компонент (домінуючий)
        color = f"#{r:02X}{g:02X}{b:02X}"
        colors.append(color)
    return colors


def bfs_iterative(root):
    """
    Обхід дерева в ширину (BFS) з використанням ЧЕРГИ.

    Алгоритм:
    1. Додаємо корінь у чергу
    2. Поки черга не порожня:
       - Витягуємо вузол з початку черги
       - Відвідуємо його (записуємо порядок)
       - Додаємо його дітей у чергу (спочатку ліве, потім праве)

    Args:
        root: Корінь дерева

    Returns:
        dict: Словник {node.id: порядок_відвідування}
    """
    if root is None:
        return {}

    order_dict = {}
    queue = deque([root])  # Черга для BFS
    counter = 0

    while queue:
        # Витягуємо вузол з початку черги
        node = queue.popleft()

        # Відвідуємо вузол
        order_dict[node.id] = counter
        counter += 1

        # Додаємо дітей у чергу
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)

    return order_dict


def dfs_iterative(root):
    """
    Обхід дерева в глибину (DFS) з використанням СТЕКУ.

    Алгоритм:
    1. Додаємо корінь у стек
    2. Поки стек не порожній:
       - Витягуємо вузол з верху стека
       - Відвідуємо його (записуємо порядок)
       - Додаємо його дітей у стек (спочатку ПРАВЕ, потім ліве)
         (це важливо для правильного порядку обходу!)

    Args:
        root: Корінь дерева

    Returns:
        dict: Словник {node.id: порядок_відвідування}
    """
    if root is None:
        return {}

    order_dict = {}
    stack = [root]  # Стек для DFS
    counter = 0

    while stack:
        # Витягуємо вузол з верху стека
        node = stack.pop()

        # Відвідуємо вузол
        order_dict[node.id] = counter
        counter += 1

        # Додаємо дітей у стек (ВАЖЛИВО: спочатку праве, потім ліве!)
        # Це потрібно, щоб ліве піддерево обробилось першим
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)

    return order_dict


def count_nodes_iterative(root):
    """
    Підраховує кількість вузлів у дереві БЕЗ рекурсії (використовує чергу).

    Args:
        root: Корінь дерева

    Returns:
        int: Кількість вузлів
    """
    if root is None:
        return 0

    count = 0
    queue = deque([root])

    while queue:
        node = queue.popleft()
        count += 1

        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)

    return count


def collect_nodes_iterative(root):
    """
    Збирає всі вузли дерева у список БЕЗ рекурсії (використовує чергу).

    Args:
        root: Корінь дерева

    Returns:
        list: Список всіх вузлів
    """
    if root is None:
        return []

    nodes_list = []
    queue = deque([root])

    while queue:
        node = queue.popleft()
        nodes_list.append(node)

        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)

    return nodes_list


def visualize_traversal(root, traversal_type="bfs"):
    """
    Візуалізує обхід дерева з кольоровим кодуванням.
    Використовує СТЕК та ЧЕРГУ, НЕ рекурсію!

    Args:
        root: Корінь дерева
        traversal_type: Тип обходу ("bfs" або "dfs")
    """
    if root is None:
        print("Дерево порожнє!")
        return

    # Підраховуємо кількість вузлів (БЕЗ рекурсії)
    n_nodes = count_nodes_iterative(root)

    # Отримуємо порядок обходу (БЕЗ рекурсії)
    if traversal_type == "bfs":
        order_dict = bfs_iterative(root)
        title = "BFS - Обхід у ширину (використовує ЧЕРГУ)"
        algorithm_desc = "Алгоритм: Черга (Queue) - FIFO (First In, First Out)"
    elif traversal_type == "dfs":
        order_dict = dfs_iterative(root)
        title = "DFS - Обхід у глибину (використовує СТЕК)"
        algorithm_desc = "Алгоритм: Стек (Stack) - LIFO (Last In, First Out)"
    else:
        raise ValueError(f"Невідомий тип обходу: {traversal_type}")

    # Генеруємо градієнт кольорів
    colors = generate_color_gradient(n_nodes)

    # Збираємо всі вузли (БЕЗ рекурсії)
    nodes_list = collect_nodes_iterative(root)

    # Призначаємо кольори вузлам відповідно до порядку обходу
    for node in nodes_list:
        order = order_dict.get(node.id, 0)
        node.color = colors[order]

    # Візуалізуємо дерево
    draw_tree(root)

    # Виводимо інформацію про обхід
    print(f"\n{title}")
    print("=" * 80)
    print(f"{algorithm_desc}")
    print("=" * 80)

    # Сортуємо вузли за порядком відвідування
    sorted_nodes = sorted(
        [(node.val, order_dict[node.id], node.color) for node in nodes_list],
        key=lambda x: x[1],
    )

    print(f"Порядок відвідування вузлів (всього {n_nodes} вузлів):")
    print(f"{'Крок':<6} {'Значення':<10} {'Колір HEX':<12} {'Опис'}")
    print("-" * 80)

    for val, order, color in sorted_nodes:
        intensity = (
            "темний"
            if order < n_nodes // 3
            else "середній"
            if order < 2 * n_nodes // 3
            else "світлий"
        )
        print(f"{order + 1:<6} {val:<10} {color:<12} ({intensity} відтінок)")


# =============================================================================
# ДЕМОНСТРАЦІЯ РОБОТИ
# =============================================================================


def create_example_tree():
    """Створює приклад дерева для демонстрації"""
    root = Node(0)
    root.left = Node(4)
    root.left.left = Node(5)
    root.left.right = Node(10)
    root.right = Node(1)
    root.right.left = Node(3)
    return root


def create_larger_tree():
    """Створює більше дерево для кращої демонстрації градієнта"""
    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.left.left = Node(4)
    root.left.right = Node(5)
    root.right.left = Node(6)
    root.right.right = Node(7)
    root.left.left.left = Node(8)
    root.left.left.right = Node(9)
    root.left.right.left = Node(10)
    return root


if __name__ == "__main__":
    print("=" * 80)
    print("ВІЗУАЛІЗАЦІЯ ОБХОДІВ БІНАРНОГО ДЕРЕВА")
    print("=" * 80)

    # Приклад 1: Базове дерево з завдання
    print("\n ПРИКЛАД 1: Базове дерево (з завдання)")
    print("-" * 80)
    tree = create_example_tree()

    print("\nСтруктура дерева:")
    print("       0")
    print("      / \\")
    print("     4   1")
    print("    / \\   \\")
    print("   5  10   3")

    # BFS обхід
    print("\n" + "=" * 80)
    print("1  ОБХІД У ШИРИНУ (BFS)")
    print("=" * 80)
    visualize_traversal(tree, "bfs")

    # DFS обхід
    print("\n" + "=" * 80)
    print("2  ОБХІД У ГЛИБИНУ (DFS)")
    print("=" * 80)
    tree = create_example_tree()  # Пересоздаємо для нових кольорів
    visualize_traversal(tree, "dfs")

    # Приклад 2: Більше дерево
    print("\n\n" + "=" * 80)
    print(" ПРИКЛАД 2: Більше дерево (для кращої візуалізації градієнта)")
    print("-" * 80)

    print("\nСтруктура дерева:")
    print("           1")
    print("         /   \\")
    print("        2     3")
    print("       / \\   / \\")
    print("      4   5 6   7")
    print("     / \\ /")
    print("    8  9 10")

    # BFS обхід
    print("\n" + "=" * 80)
    print("3  ОБХІД У ШИРИНУ (BFS) - Більше дерево")
    print("=" * 80)
    large_tree = create_larger_tree()
    visualize_traversal(large_tree, "bfs")

    # DFS обхід
    print("\n" + "=" * 80)
    print("4  ОБХІД У ГЛИБИНУ (DFS) - Більше дерево")
    print("=" * 80)
    large_tree = create_larger_tree()  # Пересоздаємо для нових кольорів
    visualize_traversal(large_tree, "dfs")
