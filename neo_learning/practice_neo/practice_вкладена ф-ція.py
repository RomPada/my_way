
# Необхідно створити функцію discount_price на Python, яка розраховує кінцеву ціну товару після застосування знижки.
# 
# Задачі:
# Створіть функцію discount_price, яка приймає два аргументи: price - початкова ціна товару та discount - знижка як дійсне число від 0 до 1.
# Усередині функції discount_price створіть вкладену функцію apply_discount, яка використовує nonlocal для доступу та модифікації змінної price.
# Функція apply_discount має обчислити знижену ціну, помноживши price на (1 - discount).
# Викличте apply_discount всередині discount_price, а потім поверніть оновлену ціну.
#
# Очікуваний результат:
# Функція повинна повертати ціну товару після застосування знижки.
# 
# Підказки:
# Використання nonlocal дозволяє функції apply_discount модифікувати змінну price, оголошену у зовнішній функції discount_price.
# Для розрахунку зниженої ціни використовуйте формулу price * (1 - discount).
 
def discount_price(price, discount):
     def apply_discount():
         nonlocal price
         price = price * (1 - discount)    
          
     apply_discount() 
     return price
