import heapq

def min_cost_to_connect_cables(cable_lengths: list[int]) -> int:
    """
    Обчислює мінімальні загальні витрати на об'єднання всіх кабелів.

    Використовує жадібний алгоритм з min-heap (чергою з пріоритетом).

    :param cable_lengths: Список початкових довжин кабелів.
    :return: Мінімальні загальні витрати.
    """
    
    # Перевірка на випадок, якщо кабелів менше двох
    if len(cable_lengths) <= 1:
        return 0

    # 1. Ініціалізація min-heap
    # heapq.heapify перетворює список на min-heap "на місці".
    # Це дозволяє швидко витягувати найменші елементи.
    heapq.heapify(cable_lengths)
    
    total_cost = 0
    
    # 2. Об'єднання кабелів, доки не залишиться лише один
    while len(cable_lengths) > 1:
        
        # 3. Витягуємо два найменші елементи (жадібний вибір)
        # heapq.heappop видаляє та повертає найменший елемент.
        cable1 = heapq.heappop(cable_lengths)
        cable2 = heapq.heappop(cable_lengths)
        
        # 4. Обчислюємо вартість об'єднання
        # Витрати дорівнюють сумі довжин кабелів, що об'єднуються.
        current_cost = cable1 + cable2
        
        # 5. Додаємо вартість до загальних витрат
        total_cost += current_cost
        
        # 6. Вставляємо новий об'єднаний кабель назад у heap
        # heapq.heappush додає елемент, зберігаючи структуру min-heap.
        heapq.heappush(cable_lengths, current_cost)
        
    return total_cost

# --- Приклад Використання ---

# Приклад з пояснення: L = [4, 3, 2, 6]
cables_a = [4, 3, 2, 6]
min_cost_a = min_cost_to_connect_cables(cables_a)

print(f"Кабелі: {cables_a}")
print(f"Мінімальні витрати: {min_cost_a}") 
# Очікуваний результат: 29 ((2+3=5) + (4+5=9) + (6+9=15) = 29)

print("-" * 20)

# Інший приклад: L = [10, 2, 5, 8]
cables_b = [12, 11, 13, 5, 6, 7]
min_cost_b = min_cost_to_connect_cables(cables_b)

print(f"Кабелі: {cables_b}")
print(f"Мінімальні витрати: {min_cost_b}")
# Розрахунок:
# 1. 2 + 5 = 7 (Витрати: 7) -> Heap: [7, 8, 10]
# 2. 7 + 8 = 15 (Витрати: 15) -> Heap: [10, 15]
# 3. 10 + 15 = 25 (Витрати: 25) -> Heap: [25]
# Загальні витрати: 7 + 15 + 25 = 47