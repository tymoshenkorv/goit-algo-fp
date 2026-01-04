"""
Завдання 1. Структури даних. Сортування. Робота з однозв'язним списком

Реалізація:
1. Функція реверсування однозв'язного списку
2. Алгоритм сортування злиттям для однозв'язного списку
3. Функція об'єднання двох відсортованих однозв'язних списків
"""


class Node:
    """Клас вузла однозв'язного списку"""

    def __init__(self, data=None):
        self.data = data
        self.next = None


class LinkedList:
    """Клас однозв'язного списку"""

    def __init__(self):
        self.head = None

    def insert_at_beginning(self, data):
        """Вставка вузла на початок списку"""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_end(self, data):
        """Вставка вузла в кінець списку"""
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = new_node

    def print_list(self):
        """Виведення списку"""
        current = self.head
        elements = []
        while current:
            elements.append(str(current.data))
            current = current.next
        print(" -> ".join(elements) if elements else "Порожній список")

    def to_list(self):
        """Конвертація в Python список для тестування"""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result


def reverse_linked_list(linked_list):
    """
    Функція для реверсування однозв'язного списку.
    Змінює посилання між вузлами.

    Алгоритм:
    - Використовуємо три покажчики: prev, current, next_node
    - Проходимо по списку та змінюємо напрямок посилань
    - Складність: O(n) за часом, O(1) за пам'яттю

    Args:
        linked_list: LinkedList об'єкт для реверсування

    Returns:
        LinkedList: реверсований список
    """
    prev = None
    current = linked_list.head

    while current:
        next_node = current.next  # Зберігаємо наступний вузол
        current.next = prev  # Змінюємо посилання на попередній
        prev = current  # Переміщуємо prev вперед
        current = next_node  # Переміщуємо current вперед

    linked_list.head = prev  # Оновлюємо голову списку
    return linked_list


def merge_sort_linked_list(linked_list):
    """
    Сортування однозв'язного списку методом злиття (Merge Sort).

    Алгоритм:
    - Рекурсивно ділимо список на дві половини
    - Сортуємо кожну половину
    - Зливаємо відсортовані половини
    - Складність: O(n log n) за часом, O(log n) за пам'яттю (рекурсія)

    Args:
        linked_list: LinkedList об'єкт для сортування

    Returns:
        LinkedList: відсортований список
    """
    if linked_list.head is None:
        return linked_list

    linked_list.head = _merge_sort_recursive(linked_list.head)
    return linked_list


def _merge_sort_recursive(head):
    """
    Рекурсивна функція для сортування злиттям.

    Args:
        head: Node - початок списку

    Returns:
        Node: початок відсортованого списку
    """
    # Базовий випадок: якщо список порожній або містить один елемент
    if head is None or head.next is None:
        return head

    # Ділимо список на дві половини
    middle = _get_middle(head)
    next_to_middle = middle.next
    middle.next = None

    # Рекурсивно сортуємо обидві половини
    left = _merge_sort_recursive(head)
    right = _merge_sort_recursive(next_to_middle)

    # Зливаємо відсортовані половини
    sorted_list = _merge_two_sorted_lists(left, right)
    return sorted_list


def _get_middle(head):
    """
    Знаходить середній вузол списку використовуючи техніку двох покажчиків.
    Повільний покажчик рухається на 1 крок, швидкий - на 2 кроки.

    Args:
        head: Node - початок списку

    Returns:
        Node: середній вузол
    """
    if head is None:
        return head

    slow = head
    fast = head

    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next

    return slow


def _merge_two_sorted_lists(left, right):
    """
    Зливає два відсортовані списки в один відсортований.
    Допоміжна функція для merge sort.

    Args:
        left: Node - перший відсортований список
        right: Node - другий відсортований список

    Returns:
        Node: початок об'єднаного відсортованого списку
    """
    # Якщо один зі списків порожній
    if left is None:
        return right
    if right is None:
        return left

    # Вибираємо менший елемент як початок результату
    if left.data <= right.data:
        result = left
        result.next = _merge_two_sorted_lists(left.next, right)
    else:
        result = right
        result.next = _merge_two_sorted_lists(left, right.next)

    return result


def merge_two_sorted_linked_lists(list1, list2):
    """
    Об'єднує два відсортовані однозв'язні списки в один відсортований список.

    Алгоритм:
    - Використовуємо два покажчики для проходу по обох списках
    - Порівнюємо елементи та додаємо менший до результату
    - Складність: O(n + m) за часом, O(1) за пам'яттю

    Args:
        list1: LinkedList - перший відсортований список
        list2: LinkedList - другий відсортований список

    Returns:
        LinkedList: об'єднаний відсортований список
    """
    # Створюємо новий список для результату
    merged_list = LinkedList()

    # Якщо обидва списки порожні
    if list1.head is None and list2.head is None:
        return merged_list

    # Якщо один зі списків порожній
    if list1.head is None:
        merged_list.head = list2.head
        return merged_list
    if list2.head is None:
        merged_list.head = list1.head
        return merged_list

    # Використовуємо допоміжну функцію для злиття
    merged_list.head = _merge_two_sorted_lists(list1.head, list2.head)

    return merged_list


# Демонстрація роботи функцій
if __name__ == "__main__":
    print("=" * 60)
    print("Завдання 1: Робота з однозв'язним списком")
    print("=" * 60)

    # Тест 1: Реверсування списку
    print("\n1. Тест реверсування списку:")
    print("-" * 60)
    llist1 = LinkedList()
    for value in [5, 10, 15, 20, 25]:
        llist1.insert_at_end(value)

    print("Оригінальний список:")
    llist1.print_list()

    reverse_linked_list(llist1)
    print("\nРеверсований список:")
    llist1.print_list()

    # Тест 2: Сортування списку
    print("\n\n2. Тест сортування списку (Merge Sort):")
    print("-" * 60)
    llist2 = LinkedList()
    for value in [64, 34, 25, 12, 22, 11, 90]:
        llist2.insert_at_end(value)

    print("Несортований список:")
    llist2.print_list()

    merge_sort_linked_list(llist2)
    print("\nВідсортований список:")
    llist2.print_list()

    # Тест 3: Об'єднання двох відсортованих списків
    print("\n\n3. Тест об'єднання двох відсортованих списків:")
    print("-" * 60)

    # Створюємо перший відсортований список
    sorted_list1 = LinkedList()
    for value in [1, 3, 5, 7, 9]:
        sorted_list1.insert_at_end(value)
    print("Перший відсортований список:")
    sorted_list1.print_list()

    # Створюємо другий відсортований список
    sorted_list2 = LinkedList()
    for value in [2, 4, 6, 8, 10]:
        sorted_list2.insert_at_end(value)
    print("\nДругий відсортований список:")
    sorted_list2.print_list()

    # Об'єднуємо списки
    merged = merge_two_sorted_linked_lists(sorted_list1, sorted_list2)
    print("\nОб'єднаний відсортований список:")
    merged.print_list()

    # Тест 4: Додатковий тест з різними розмірами списків
    print("\n\n4. Додатковий тест (списки різних розмірів):")
    print("-" * 60)

    list_a = LinkedList()
    for value in [1, 5, 10]:
        list_a.insert_at_end(value)
    print("Список A:")
    list_a.print_list()

    list_b = LinkedList()
    for value in [2, 3, 4, 6, 7, 8, 9]:
        list_b.insert_at_end(value)
    print("\nСписок B:")
    list_b.print_list()

    merged2 = merge_two_sorted_linked_lists(list_a, list_b)
    print("\nОб'єднаний список:")
    merged2.print_list()

    # Тест 5: Комплексний тест - сортування та об'єднання
    print("\n\n5. Комплексний тест (сортування + об'єднання):")
    print("-" * 60)

    unsorted1 = LinkedList()
    for value in [5, 2, 8, 1]:
        unsorted1.insert_at_end(value)
    print("Несортований список 1:")
    unsorted1.print_list()

    unsorted2 = LinkedList()
    for value in [9, 3, 7, 4]:
        unsorted2.insert_at_end(value)
    print("\nНесортований список 2:")
    unsorted2.print_list()

    # Сортуємо обидва списки
    merge_sort_linked_list(unsorted1)
    merge_sort_linked_list(unsorted2)

    print("\nПісля сортування:")
    print("Список 1:")
    unsorted1.print_list()
    print("\nСписок 2:")
    unsorted2.print_list()

    # Об'єднуємо відсортовані списки
    final_merged = merge_two_sorted_linked_lists(unsorted1, unsorted2)
    print("\nФінальний об'єднаний список:")
    final_merged.print_list()

    print("\n" + "=" * 60)
    print("Всі тести завершено успішно!")
    print("=" * 60)
