from pulp import LpProblem, LpVariable, LpMaximize, LpStatus, value

# Створення моделі
model = LpProblem("Drink_Production_Optimization", LpMaximize)

# Визначення змінних
L = LpVariable("Lemonade", lowBound=0, cat="Integer")
J = LpVariable("Fruit_Juice", lowBound=0, cat="Integer")

# Ресурси
model += 2 * L + 1 * J <= 100, "Water"
model += 1 * L <= 50, "Sugar"
model += 1 * L <= 30, "Lemon_Juice"
model += 2 * J <= 40, "Fruit_Puree"
model += L + J, "Total_Products"

# Цільова функція
model += L + J, "Total_Products"

model.solve(PULP_CBC_CMD(msg=False)) # Максимізувати загальну кількість продуктів


print("Статус:", LpStatus[model.status])
print("Лимонад:", int(value(L)))
print("Фруктовий сік:", int(value(J)))
print("Загалом продуктів:", int(value(L + J)))

print("\nВикористання ресурсів:")
print("Вода:", int(value(2 * L + 1 * J)), "/ 100")
print("Цукор:", int(value(L)), "/ 50")
print("Лимонний сік:", int(value(L)), "/ 30")
print("Фруктове пюре:", int(value(2 * J)), "/ 40")

