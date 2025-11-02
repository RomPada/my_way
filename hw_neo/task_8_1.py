
def caching_fibonacci():    # Ф-ція caching_fibonacci
    cache = {}              # Створюємо порожній словник 
    def fibonacci(n: int):       # Ф-ція fibonacci яка приймає аргумент (n)
        if n in cache:      # Якщо n у cache, повертаємо cache[n]
            return cache[n]
        elif n <= 0:        # Якщо n <= 0, повертаємо 0
            return 0
        elif n == 1:        # Якщо n == 1, повертаємо 1
            return 1
        else:
            cache[n] = fibonacci(n - 1) + fibonacci(n - 2) # Формула Фібоначі
            return cache[n] # Повертаємо cache[n]
    return fibonacci        # Повертаємо ф-цію fibonacci
# Кінець ф-ції caching_fibonacci

# Отримуємо ф-цію fibonacci
fib = caching_fibonacci()

# Використовуємо ф-цію fibonacci для обчислення чисел Фібоначчі
print(fib(10))  # Виведе 55
print(fib(15))  # Виведе 610
