
min = 1
max = 49
quantity = 6


def get_numbers_ticket(min, max, quantity):
    import random
    list_number = list() # створюємо список
    if min >= 1 and max <= 1000 and min < quantity < max: 
    
        # виконую задачу не через get_numbers_ticket, як у рекомендаціях до завдання, а своїм способом
        list_number.extend(random.sample(range(min, max), quantity)) # додаємо у список рандомні унікальні числа з виборки
        list_number.sort() # сортуємо від меншого до більшого
        print(list_number)
        return list_number
    else: # Якщо параметри не відповідають заданим обмеженням, функція повертає пустий список.
        print(list_number)
        return list_number
    
    
get_numbers_ticket(min, max, quantity)
