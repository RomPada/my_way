
# Команда break зупиняє цикл в момент виклику і не завершує ітерацію.
for number in [1, 2, 3, 4, 5]:
    if number == 3:
        break
    print(number)
print("Кінець") # 1 2 Кінець


# Аби одразу перейти до наступної ітерації циклу без виконання виразів, що залишилися, є команда continue
for number in [1, 2, 3, 4, 5]:
    if number == 3:
        continue
    print(number)
print("Кінець") # 1 2 4 5 Кінець


#####
x = 0
while x < 5:
    x += 1
    if x == 3:
        continue
    if x == 5:
        break
    print(x) # 1 2 4