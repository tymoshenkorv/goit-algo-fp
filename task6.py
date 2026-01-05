# Завдання 6. Жадібні алгоритми та динамічне програмування

# Необхідно написати програму на Python, яка використовує два підходи — жадібний алгоритм та алгоритм динамічного програмування для розв’язання
# задачі вибору їжі з найбільшою сумарною калорійністю в межах обмеженого бюджету.
# Кожен вид їжі має вказану вартість і калорійність. Дані про їжу представлені у вигляді словника, де ключ — назва страви,
# а значення — це словник з вартістю та калорійністю.

# items = {
#     "pizza": {"cost": 50, "calories": 300},
#     "hamburger": {"cost": 40, "calories": 250},
#     "hot-dog": {"cost": 30, "calories": 200},
#     "pepsi": {"cost": 10, "calories": 100},
#     "cola": {"cost": 15, "calories": 220},
#     "potato": {"cost": 25, "calories": 350}
# }

# Розробіть функцію greedy_algorithm жадібного алгоритму, яка вибирає страви, максимізуючи співвідношення калорій до вартості,
# не перевищуючи заданий бюджет. # Для реалізації алгоритму динамічного програмування створіть функцію dynamic_programming,
# яка обчислює оптимальний набір страв для максимізації калорійності при заданому бюджеті.


def greedy_algorithm(items, budget):
    """
    Жадібний алгоритм для вибору страв з максимальною калорійністю.

    Стратегія: вибираємо страви з найкращим співвідношенням калорії/вартість

    Args:
        items: словник з стравами {назва: {"cost": вартість, "calories": калорії}}
        budget: доступний бюджет

    Returns:
        tuple: (список вибраних страв, загальна вартість, загальні калорії)
    """
    # Обчислюємо співвідношення калорії/вартість для кожної страви
    items_ratio = []
    for name, info in items.items():
        ratio = info["calories"] / info["cost"]
        items_ratio.append((name, info["cost"], info["calories"], ratio))

    # Сортуємо за співвідношенням (від найбільшого до найменшого)
    items_ratio.sort(key=lambda x: x[3], reverse=True)

    selected_items = []
    total_cost = 0
    total_calories = 0

    # Жадібно вибираємо страви поки вистачає бюджету
    for name, cost, calories, ratio in items_ratio:
        if total_cost + cost <= budget:
            selected_items.append(name)
            total_cost += cost
            total_calories += calories

    return selected_items, total_cost, total_calories


def dynamic_programming(items, budget):
    """
    Алгоритм динамічного програмування для оптимального вибору страв.

    Args:
        items: словник з стравами {назва: {"cost": вартість, "calories": калорії}}
        budget: доступний бюджет

    Returns:
        tuple: (список вибраних страв, загальна вартість, загальні калорії)
    """
    # Перетворюємо словник у список для зручності
    items_list = [
        (name, info["cost"], info["calories"]) for name, info in items.items()
    ]
    n = len(items_list)

    # Створюємо таблицю DP: dp[i][w] = максимальні калорії
    # з перших i страв при бюджеті w
    dp = [[0 for _ in range(budget + 1)] for _ in range(n + 1)]

    # Заповнюємо таблицю DP
    for i in range(1, n + 1):
        name, cost, calories = items_list[i - 1]
        for w in range(budget + 1):
            # Не беремо поточну страву
            dp[i][w] = dp[i - 1][w]

            # Якщо можемо взяти поточну страву, вибираємо максимум
            if cost <= w:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - cost] + calories)

    # Відновлюємо вибрані страви
    selected_items = []
    total_calories = dp[n][budget]
    w = budget

    for i in range(n, 0, -1):
        # Якщо калорійність змінилась, значить цю страву взяли
        if dp[i][w] != dp[i - 1][w]:
            name, cost, calories = items_list[i - 1]
            selected_items.append(name)
            w -= cost

    total_cost = sum(items[name]["cost"] for name in selected_items)

    return selected_items, total_cost, total_calories


def print_results(title, selected_items, total_cost, total_calories, items):
    """Виводить результати у форматованому вигляді"""
    print(f"\n{title}")
    print("=" * 60)
    print(f"Вибрані страви: {', '.join(selected_items)}")
    print(f"Загальна вартість: {total_cost}")
    print(f"Загальна калорійність: {total_calories}")
    print("\nДеталі:")
    for item in selected_items:
        print(
            f"  - {item}: вартість {items[item]['cost']}, "
            f"калорії {items[item]['calories']}, "
            f"співвідношення {items[item]['calories'] / items[item]['cost']:.2f}"
        )


if __name__ == "__main__":
    # Дані про їжу
    items = {
        "pizza": {"cost": 50, "calories": 300},
        "hamburger": {"cost": 40, "calories": 250},
        "hot-dog": {"cost": 30, "calories": 200},
        "pepsi": {"cost": 10, "calories": 100},
        "cola": {"cost": 15, "calories": 220},
        "potato": {"cost": 25, "calories": 350},
    }

    # Тестові бюджети
    budgets = [50, 100, 150]

    for budget in budgets:
        print(f"\n{'#' * 60}")
        print(f"БЮДЖЕТ: {budget}")
        print(f"{'#' * 60}")

        # Жадібний алгоритм
        greedy_items, greedy_cost, greedy_calories = greedy_algorithm(items, budget)
        print_results(
            "ЖАДІБНИЙ АЛГОРИТМ", greedy_items, greedy_cost, greedy_calories, items
        )

        # Динамічне програмування
        dp_items, dp_cost, dp_calories = dynamic_programming(items, budget)
        print_results("ДИНАМІЧНЕ ПРОГРАМУВАННЯ", dp_items, dp_cost, dp_calories, items)


