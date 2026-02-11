from decimal import Decimal

print(Decimal("0.1") + Decimal("0.2") == Decimal("0.3")) # True
print(Decimal("0.1") + Decimal("0.2")) # 0.3

###
# getcontext встановлює кількість значущих цифр.
from decimal import Decimal, getcontext

getcontext().prec = 6
print(Decimal("1") / Decimal("7"))

getcontext().prec = 8
print(Decimal("1") / Decimal("7"))


###
# округлити число до двох знаків після коми, використовуєте Decimal об'єкт з двома нулями після коми як шаблон
import decimal
from decimal import Decimal
 
number = Decimal("1.45")

# Округлення за замовчуванням до одного десяткового знаку # Округлення за замовчуванням ROUND_HALF_EVEN: 1.4
print("Округлення за замовчуванням ROUND_HALF_EVEN:", number.quantize(Decimal("0.0"))) 

# Округлення вверх при нічиї (ROUND_HALF_UP) # Округлення вгору ROUND_HALF_UP: 1.5
print("Округлення вгору ROUND_HALF_UP:", number.quantize(Decimal("0.0"), rounding=decimal.ROUND_HALF_UP))

# Округлення вниз (ROUND_FLOOR) # Округлення вниз ROUND_FLOOR: 1.4
print("Округлення вниз ROUND_FLOOR:", number.quantize(Decimal("0.0"), rounding=decimal.ROUND_FLOOR))

# Округлення вверх (ROUND_CEILING) # Округлення вгору ROUND_CEILING: 1.5
print("Округлення вгору ROUND_CEILING:", number.quantize(Decimal("0.0"), rounding=decimal.ROUND_CEILING))

# Округлення до трьох десяткових знаків за замовчуванням # Округлення до трьох десяткових знаків: 3.142
print("Округлення до трьох десяткових знаків:", Decimal("3.14159").quantize(Decimal("0.000")))
