import random

# кількість симуляцій (кидків двох кубиків)
N = 500_000

# словник для підрахунку сум від 2 до 12
counts = {s: 0 for s in range(2, 13)}

# симуляція кидків
for _ in range(N):
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    total = dice1 + dice2
    counts[total] += 1

# обчислення ймовірностей
probabilities = {
    s: counts[s] / N for s in counts
}


print("Сума | Ймовірність (Монте-Карло)")
print("-" * 30)

for s in range(2, 13):
    print(f"{s:>4} | {probabilities[s]*100:6.2f}%")

