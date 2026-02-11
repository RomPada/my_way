
raw_numbers = [
    "067\\t123 4567",
     "    +38(050)123-32-34",
    "     0503451234",
    "(050)8889900",
    "38050-111-22-22",
    "38050 111 22 11   ",
    "    +38(050)123-32-34",
    "     0503451234",
    "(050)8889900",
    "38050-111-22-22",
    "38050 111 22 11   ",
    "(095) 234-5678\\n",
    "+380 44 123 4567",
    "380501234567"
    ]


def replace (raw_numbers): 
    raw_good_numbers = [] # створюємо список фінальних упорядкованих номерів телефонів
    index = 0 
    while index < len(raw_numbers): # ф-ція працює доки не пройде по кожному номеру телефона (індексу) => рядок 44
        element = raw_numbers[index] # елемент це неупорядкований номер телефону
        new_element = str(element) # переводимо номер телфону у рядок
        def change(new_element): 
            index_2 = 0
            dictionary = ["+", "\\", " ", "-", "(", ")", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]  # словник що лишнє ми прибираємо
            while index_2 < len(dictionary): # ф-ція працює доки не перебере весь словник => рядок 31
                change = dictionary[index_2] # заміна на кожен елемент словника
                new_element = new_element.replace(change, "")  # всі елементи зі словника видаляємо шлязом заміни на "нічого"
                index_2 += 1
            return new_element  # повертаємо номер теелфону без лишніх символів
        new_element = change(new_element)
        def normalize(new_element):  # ф-ція додавання +380. в цілому вся фунція побудована на визначенні к-сті цифр, та, як наслідок, додаванні відповідної необхідної кількоості правильних цифр та плюса
            if len(new_element) == 12:
                new_element = "+" + new_element
            if len(new_element) == 11:
                new_element = "+3" + new_element
            if len(new_element) == 10:
                new_element = "+38" + new_element
            return new_element   
        new_element = normalize(new_element)
        raw_good_numbers.append(new_element)  # результати додаємо у новий список
        index += 1
    print("Нормалізовані номери телефонів для SMS-розсилки:", raw_good_numbers) # вивід функції відповідно до прикладу у задачі


replace (raw_numbers)
