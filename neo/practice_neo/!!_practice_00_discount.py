# Розглянемо типову задачу, яка відображає реальну ситуацію в області торгівлі та фінансів, де потрібно часто обраховувати 
# ціни зі знижками. Нам необхідно створити функцію для розрахунку вартості товарів з урахуванням можливої знижки.

# Для розрахунку реальної ціни з врахуванням дисконту створимо функцію real_cost. Функція real_cost повинна приймати два 
# аргументи: базову ціну товару base та розмір знижки discount, який за замовчуванням будемо вважати 0. Вона повинна 
# повертати вартість товару після застосування знижки.





































































# def real_cost(base: int, discount: float = 0) -> float:
#     return base * (1 - discount)
# price_bread = 15
# price_butter = 50
# price_sugar = 60

# current_price_bread = real_cost(price_bread)
# current_price_butter = real_cost(price_butter, 0.05)
# current_price_sugar = real_cost(price_sugar, 0.07)

# print(f'Нова вартість хліба: {current_price_bread}')
# print(f'Нова вартість масла: {current_price_butter}')
# print(f'Нова вартість цукру: {current_price_sugar}')

# Нова вартість хліба: 15
# Нова вартість масла: 47.5
# Нова вартість цукру: 55.8

######

# def apply_discount(price: float, discount_percentage: int) -> float:
#     return price * (1 - discount_percentage / 100)

# # Використання
# discounted_price = apply_discount(500, 10)  # Знижка 10% на ціну 500
# print(discounted_price)

# discounted_price = apply_discount(500, 20)  # Знижка 20% на ціну 500
# print(discounted_price)