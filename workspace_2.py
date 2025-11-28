from queue import Queue
import random
import time
import threading

queue = Queue()

def generate_request():
    while True:  # змінено: виніс безкінечний цикл у сам потік генерації
        wait_time = random.uniform(0.5, 1.0)
        time.sleep(wait_time)
        request_id = random.randint(1000, 9999)
        queue.put(request_id)
        print(f"Створено заявку з ID: {request_id}")

def process_request():
    while True:  # змінено: виніс безкінечний цикл у потік обробки
        wait_time = random.uniform(0.5, 0.8)
        time.sleep(wait_time)
        if not queue.empty():
            request_id = queue.get()
            print(f"Оброблено заявку з ID: {request_id}")
        else:
            print("Черга порожня.")

def main(): 
    # створюємо потоки ОДИН раз і запускаємо їх
    t1 = threading.Thread(target=generate_request, daemon=True)  # змінено: створюємо потік генерації + daemon=True
    t2 = threading.Thread(target=process_request, daemon=True)  # змінено: створюємо потік обробки + daemon=True

    t1.start()  # змінено: запускаємо потік генерації поза циклом
    t2.start()  # змінено: запускаємо потік обробки поза циклом

    try:
        while True:
            time.sleep(0.1)  # змінено: головний потік просто "живе", щоб програма не завершувалась
    except KeyboardInterrupt:
        print("\nЗупинка обробки заявок...")

if __name__ == "__main__":
    main()
