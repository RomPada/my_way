
count_cruasan = int(input("Введіть кількість круасанів: "))
prise_cruasan = 1.04
cost_cruasan = count_cruasan * prise_cruasan

count_glass = int(input("Введіть кількість стаканчиків: "))
prise_glass = 0.34
cost_glass = count_glass * prise_glass

count_coffee = int(input("Введіть кількість пакунків кави: "))
prise_coffee = 4.42
cost_coffee = count_coffee * prise_coffee

Cost = float(cost_cruasan + cost_glass + cost_coffee)
Dol = int(Cost)
Cent = (Cost - Dol) * 100
print(f"Загальна вартість {Cost:.2f} ({int(Cost)} долари та {Cent:.0f} центів)")
