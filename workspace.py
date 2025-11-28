from queue import Queue
import random
import time

queue = Queue()

def generate_request():
    request_id = random.randint(1000, 9999)
    queue.put(request_id)
    print(f"Створено заявку з ID: {request_id}")

def process_request():
    if not queue.empty():
        request_id = queue.get()
        print(f"Оброблено заявку з ID: {request_id}")
    else:
        print("Черга порожня.")

def main(): 
    try:
        while True:
            time.sleep(random.uniform(0.7, 1.5))
            generate_request()
            process_request()
    except KeyboardInterrupt:
        print("\nЗупинка обробки заявок...")

if __name__ == "__main__":
    main()
