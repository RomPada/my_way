import heapq

def min_connection_cost(cables):
    heap = cables[:]          # копія списку
    heapq.heapify(heap)       # перетворюємо у мін-купу

    total = 0
    steps = []                # щоб бачити порядок (не обов'язково)

    while len(heap) > 1:
        a = heapq.heappop(heap)
        b = heapq.heappop(heap)
        cost = a + b
        total += cost
        steps.append((a, b, cost))
        heapq.heappush(heap, cost)

    return total, steps

# приклад
cables = [5, 6, 7, 11, 12, 13]
total, steps = min_connection_cost(cables)

print("Загальні витрати:", total)
print("Кроки:")
for a, b, cost in steps:
    print(f"{a} + {b} = {cost}")
