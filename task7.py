# Завдання 7. Використання методу Монте-Карло

# Необхідно написати програму на Python, яка імітує велику кількість кидків кубиків, обчислює суми чисел, які випадають на кубиках, і визначає ймовірність кожної можливої суми.
# Створіть симуляцію, де два кубики кидаються велику кількість разів. Для кожного кидка визначте суму чисел, які випали на обох кубиках. Підрахуйте, скільки разів кожна можлива сума (від 2 до 12) з’являється у процесі симуляції. Використовуючи ці дані, обчисліть імовірність кожної суми.
# На основі проведених імітацій створіть таблицю або графік, який відображає ймовірності кожної суми, виявлені за допомогою методу Монте-Карло.

# Таблиця ймовірностей сум при киданні двох кубиків виглядає наступним чином.
# | Сума на кубиках | Ймовірність (%) |
# |-----------------|-----------------|
# |        2        |      2.78       |
# |        3        |      5.56       |
# |        4        |      8.33       |
# |        5        |     11.11       |
# |        6        |     13.89       |
# |        7        |     16.67       |
# |        8        |     13.89       |
# |        9        |     11.11       |
# |       10        |      8.33       |
# |       11        |      5.56       |
# |       12        |      2.78       |

# Порівняйте отримані за допомогою методу Монте-Карло результати з аналітичними розрахунками, наведеними в таблиці вище.

import random
from collections import defaultdict
import matplotlib.pyplot as plt


def simulate_dice_rolls(num_simulations=100000):
    """
    Симулює кидання двох кубиків задану кількість разів.

    Args:
        num_simulations (int): Кількість симуляцій кидків

    Returns:
        dict: Словник з сумами та їх частотами
    """
    results = defaultdict(int)

    for _ in range(num_simulations):
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        dice_sum = dice1 + dice2
        results[dice_sum] += 1

    return results


def calculate_probabilities(results, num_simulations):
    """
    Обчислює ймовірності для кожної суми.

    Args:
        results (dict): Результати симуляцій
        num_simulations (int): Загальна кількість симуляцій

    Returns:
        dict: Словник з ймовірностями для кожної суми
    """
    probabilities = {}

    for dice_sum in range(2, 13):
        count = results.get(dice_sum, 0)
        probabilities[dice_sum] = (count / num_simulations) * 100

    return probabilities


def get_analytical_probabilities():
    """
    Повертає аналітичні ймовірності для кожної суми двох кубиків.

    Returns:
        dict: Словник з теоретичними ймовірностями
    """
    # Кількість комбінацій для кожної суми
    combinations = {
        2: 1,  # (1,1)
        3: 2,  # (1,2), (2,1)
        4: 3,  # (1,3), (2,2), (3,1)
        5: 4,  # (1,4), (2,3), (3,2), (4,1)
        6: 5,  # (1,5), (2,4), (3,3), (4,2), (5,1)
        7: 6,  # (1,6), (2,5), (3,4), (4,3), (5,2), (6,1)
        8: 5,  # (2,6), (3,5), (4,4), (5,3), (6,2)
        9: 4,  # (3,6), (4,5), (5,4), (6,3)
        10: 3,  # (4,6), (5,5), (6,4)
        11: 2,  # (5,6), (6,5)
        12: 1,  # (6,6)
    }

    total_combinations = 36
    probabilities = {}

    for dice_sum, count in combinations.items():
        probabilities[dice_sum] = (count / total_combinations) * 100

    return probabilities


def print_comparison_table(monte_carlo_prob, analytical_prob):
    """
    Виводить таблицю порівняння результатів Монте-Карло та аналітичних розрахунків.

    Args:
        monte_carlo_prob (dict): Ймовірності з симуляції
        analytical_prob (dict): Теоретичні ймовірності
    """
    print("\n" + "=" * 70)
    print("ПОРІВНЯННЯ РЕЗУЛЬТАТІВ МОНТЕ-КАРЛО ТА АНАЛІТИЧНИХ РОЗРАХУНКІВ")
    print("=" * 70)
    print(f"{'Сума':^6} | {'Монте-Карло':^15} | {'Аналітичний':^15} | {'Різниця':^12}")
    print("-" * 70)

    for dice_sum in range(2, 13):
        mc_prob = monte_carlo_prob[dice_sum]
        an_prob = analytical_prob[dice_sum]
        difference = abs(mc_prob - an_prob)

        print(
            f"{dice_sum:^6} | {mc_prob:>14.2f}% | {an_prob:>14.2f}% | {difference:>11.4f}%"
        )

    print("=" * 70)


def plot_probabilities(monte_carlo_prob, analytical_prob, num_simulations):
    """
    Створює графік порівняння ймовірностей.

    Args:
        monte_carlo_prob (dict): Ймовірності з симуляції
        analytical_prob (dict): Теоретичні ймовірності
        num_simulations (int): Кількість симуляцій
    """
    sums = list(range(2, 13))
    mc_values = [monte_carlo_prob[s] for s in sums]
    an_values = [analytical_prob[s] for s in sums]

    plt.figure(figsize=(12, 6))

    x = range(len(sums))
    width = 0.35

    plt.bar(
        [i - width / 2 for i in x],
        mc_values,
        width,
        label="Монте-Карло",
        alpha=0.8,
        color="skyblue",
    )
    plt.bar(
        [i + width / 2 for i in x],
        an_values,
        width,
        label="Аналітичний розрахунок",
        alpha=0.8,
        color="lightcoral",
    )

    plt.xlabel("Сума на кубиках", fontsize=12)
    plt.ylabel("Ймовірність (%)", fontsize=12)
    plt.title(
        f"Порівняння ймовірностей сум при киданні двох кубиків\n"
        f"(Кількість симуляцій: {num_simulations:,})",
        fontsize=14,
    )
    plt.xticks(x, sums)
    plt.legend()
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()

    # Зберігаємо графік
    plt.savefig("task7_monte_carlo_comparison.png", dpi=300, bbox_inches="tight")
    print("\nГрафік збережено як 'task7_monte_carlo_comparison.png'")

    plt.show()


def calculate_average_error(monte_carlo_prob, analytical_prob):
    """
    Обчислює середню похибку між результатами Монте-Карло та аналітичними розрахунками.

    Args:
        monte_carlo_prob (dict): Ймовірності з симуляції
        analytical_prob (dict): Теоретичні ймовірності

    Returns:
        float: Середня абсолютна похибка
    """
    errors = []
    for dice_sum in range(2, 13):
        error = abs(monte_carlo_prob[dice_sum] - analytical_prob[dice_sum])
        errors.append(error)

    return sum(errors) / len(errors)


def main():
    """
    Головна функція для виконання симуляції та виведення результатів.
    """
    # Кількість симуляцій
    num_simulations = 1000000

    print(f"\nВиконується симуляція {num_simulations:,} кидків двох кубиків...")

    # Виконання симуляції
    results = simulate_dice_rolls(num_simulations)

    # Обчислення ймовірностей
    monte_carlo_prob = calculate_probabilities(results, num_simulations)
    analytical_prob = get_analytical_probabilities()

    # Виведення таблиці порівняння
    print_comparison_table(monte_carlo_prob, analytical_prob)

    # Обчислення середньої похибки
    avg_error = calculate_average_error(monte_carlo_prob, analytical_prob)
    print(f"\nСередня абсолютна похибка: {avg_error:.4f}%")

    # Побудова графіка
    plot_probabilities(monte_carlo_prob, analytical_prob, num_simulations)

    # Висновки
    print("\n" + "=" * 70)
    print("ВИСНОВКИ:")
    print("=" * 70)
    print("1. Метод Монте-Карло дає результати, які дуже близькі до")
    print("   теоретичних ймовірностей.")
    print(
        f"2. При {num_simulations:,} симуляціях середня похибка становить {avg_error:.4f}%."
    )
    print("3. Найбільш ймовірна сума - 7 (16.67%), найменш ймовірні - 2 і 12 (2.78%).")
    print("4. Збільшення кількості симуляцій покращує точність результатів.")
    print("5. Розподіл ймовірностей є симетричним відносно суми 7.")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
