
# Приклад функції, що повертає рядок
def greet(name: str) -> str:
    return f"Привіт, {name}!"

greeting = greet("Олексій")
print(greeting)  # Виведе: Привіт, Олексій!


# Приклад функції, яка сумує два числа та повертає результат
def add_numbers(num1: int, num2: int) -> int:
    sum = num1 + num2
    return sum

result = add_numbers(5, 10)
print(result)  # Виведе: 15


# Функція, що повертає булеве значення:
def is_even(num: int) -> bool:
    return num % 2 == 0

check_even = is_even(4)
print(check_even)  # Виведе: True


# функція зі значеннями за замовчуванням
def func(a, b=5, c=10): 
    print('a дорівнює', a,', b дорівнює', b,', а c дорівнює', c)
# a дорівнює 3, b дорівнює 7, а c дорівнює 10
func(3, 7)
# a дорівнює 25, b дорівнює 5, а c дорівнює 24
func(25, c=24)
# a дорівнює 100, b дорівнює 5, а c дорівнює 50
func(c=50, a=100)


#####
# Замикання відбувається, коли внутрішня функція запам'ятовує стан свого оточення в момент свого створення і може 
# використовувати ці змінні навіть після того, як зовнішня функція завершила своє виконання.
# Каунтер виклику функції
from typing import Callable

def counter() -> Callable[[], int]:
    count = 0
    def increment() -> int:
        # використовуємо nonlocal, щоб змінити змінну в замиканні
        nonlocal count  
        count += 1
        return count
    return increment

# Створення лічильника
count_calls = counter()

# Виклики лічильника
print(count_calls())  # Виведе 1
print(count_calls())  # Виведе 2
print(count_calls())  # Виведе 3


#####
# Каррінг (currying) — це техніка в програмуванні, коли функція, яка приймає кілька аргументів, 
# перетворюється на послідовність функцій, кожна з яких приймає один аргумент.

# Тут функція add приймає перший аргумент a і повертає функцію add_b. 
# Сама функція add_b приймає другий аргумент b і повертає результат a + b. 
# Фактично ми перетворили виклик функції add на виклик двох функцій.
def add(a):
    def add_b(b):
        return a + b
    return add_b

# Використання:
add_5 = add(5)
result = add_5(10)
print(result)

# функція для обчислення знижки на товар після карінгу
from typing import Callable

def discount(discount_percentage: int) -> Callable[[float], float]:
    def apply_discount(price: float) -> float:
        return price * (1 - discount_percentage / 100)
    return apply_discount

# Каррінг в дії
ten_percent_discount = discount(10)
twenty_percent_discount = discount(20)

# Застосування знижок
discounted_price = ten_percent_discount(500)  # 450.0
print(discounted_price)

discounted_price = twenty_percent_discount(500)  # 400.0
print(discounted_price)