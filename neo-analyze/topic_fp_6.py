items = {
    "pizza": {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog": {"cost": 30, "calories": 200},
    "pepsi": {"cost": 10, "calories": 100},
    "cola": {"cost": 15, "calories": 220},
    "potato": {"cost": 25, "calories": 350}
}


# Жадібний алгоритм
def greedy_algorithm(items: dict, budget: int):
    ranked = sorted(
        items.items(),
        key=lambda item: item[1]["calories"] / item[1]["cost"],
        reverse=True
    )

    chosen = []
    total_cost = 0
    total_calories = 0

    for name, info in ranked:
        if total_cost + info["cost"] <= budget:
            chosen.append(name)
            total_cost += info["cost"]
            total_calories += info["calories"]
    return chosen, total_cost, total_calories


# Динамічне програмування
def dynamic_programming(items: dict, budget: int):
    names = list(items.keys())
    n = len(names)

    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        name = names[i - 1]
        cost = items[name]["cost"]
        calories = items[name]["calories"]

        for b in range(budget + 1):
            dp[i][b] = dp[i - 1][b]

            if cost <= b:
                dp[i][b] = max(
                    dp[i][b],
                    dp[i - 1][b - cost] + calories
                )

# Відновлення набору
    chosen = []
    b = budget
    for i in range(n, 0, -1):
        if dp[i][b] != dp[i - 1][b]:
            name = names[i - 1]
            chosen.append(name)
            b -= items[name]["cost"]

    chosen.reverse()
    total_calories = dp[n][budget]
    total_cost = sum(items[name]["cost"] for name in chosen)

    return chosen, total_cost, total_calories


# Ввід бюджету користувачем
while True:
    try:
        budget = int(input("Введіть ваш бюджет (наприклад 100): "))
        if budget <= 0:
            print("Бюджет має бути додатнім числом.")
            continue
        break
    except ValueError:
        print("Будь ласка, введіть число.")


# Виконання жадібного алгоритму та динамічного програмування
g_items, g_cost, g_cal = greedy_algorithm(items, budget)
d_items, d_cost, d_cal = dynamic_programming(items, budget)

print("\nЖАДІБНИЙ АЛГОРИТМ:")
print("Обрані страви:", g_items)
print("Загальна вартість:", g_cost)
print("Загальні калорії:", g_cal)

print("\nДИНАМІЧНЕ ПРОГРАМУВАННЯ (ОПТИМАЛЬНО):")
print("Обрані страви:", d_items)
print("Загальна вартість:", d_cost)
print("Загальні калорії:", d_cal)

