from queue import Queue
import random
from time import sleep

class Request:
    def __init__(self):
        self.id = random.randrange(1, 1_000_000)
    def __str__(self):
        return f"Request ID: {self.id}"

#Створити чергу заявок
queue = Queue()

def generate_request():
    #Створити нову заявку
    new_request = Request()
    #Додати заявку до черги
    queue.put(new_request)

def process_request():
    #Якщо черга не пуста:
    if not queue.empty():
        #Видалити заявку з черги
        request = queue.get()
        #Обробити заявку
        print(request)
        # Імітую бурхливу обробку запиту
        sleep(1)
    #Інакше:
    else:
        #Вивести повідомлення, що черга пуста
        print("The queue is empty.")

def main():
    try:
        #Головний цикл програми:
        while True:
            #Виконати generate_request() для створення нових заявок
            generate_request()
            #Виконати process_request() для обробки заявок
            process_request()
    except KeyboardInterrupt:
        #Поки користувач не вийде з програми:
        print("\nManual stopping processing requests...")

if __name__ == "__main__":
        main()