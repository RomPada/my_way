from queue import Queue
import time
import random

# Створюємо чергу заявок
request_queue = Queue()

def generate_request(request_id):
    """
    Функція генерує нову заявку та додає її до черги.
    """
    # Створюємо "заявку" як словник з даними
    new_request = {
        "id": request_id,
        "data": f"Заявка №{request_id}"
    }
    
    request_queue.put(new_request)
    print(f"[Generating] Створено та додано: {new_request['data']}")

def process_request():
    """
    Функція обробляє заявку: видаляє її з черги, якщо вона не пуста.
    """
    if not request_queue.empty():
        # Видаляємо заявку з черги (FIFO - First In, First Out)
        current_request = request_queue.get()
        
        print(f"[Processing] Обробляється: {current_request['data']}...")
        # Імітація часу, потрібного на обробку
        time.sleep(1) 
        print(f"[Done] {current_request['data']} оброблено.")
    else:
        print("[Queue Empty] Черга пуста. Очікування нових заявок...")

def main():
    request_id_counter = 1
    
    print("Система обробки заявок запущена. Натисніть Ctrl+C для виходу.")
    print("-" * 50)

    try:
        while True:
            # Імітуємо ймовірність створення нової заявки
            # (іноді заявки надходять швидше, ніж обробляються)
            if random.random() > 0.3:  # 70% шанс появи заявки
                generate_request(request_id_counter)
                request_id_counter += 1
            
            # Спробувати обробити заявку
            process_request()
            
            # Коротка пауза між ітераціями циклу для наочності
            time.sleep(0.5)
            print("-" * 20)

    except KeyboardInterrupt:
        print("\nРоботу програми завершено користувачем.")

if __name__ == "__main__":
    main()