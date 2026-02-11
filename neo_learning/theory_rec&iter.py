
# Рекурсивна версія
def sum_rec(n):
    if n == 0: # базовий випадок
        return 0
    else:
        return n + sum_rec(n - 1) # рекурсивний випадок

print(sum_rec(5)) # виведе 15


# Ітеративна версія
def sum_iter(n):
    result = 0
    for i in range(1, n + 1):
        result += i
    return result

print(sum_iter(5)) # виведе 15
