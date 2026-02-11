
# Копіювання об'єкту без зміни оригіналу
import copy

a = 2
b = a 
c = copy.deepcopy(a)
c = c + 1

print(a,b, c)

#####
# Для пошуку деякого символу або підрядка у рядку можна скористатися методом find:

s = "Hi there!"

start = 0
end = 7

print(s.find("er", start, end)) # 5
print(s.find("q")) # -1
