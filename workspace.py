import queue
import time
import random

# Створюємо чергу
request_queue = queue.Queue()

# Лічильник для генерації унікальних заявок
request_id = 0

def generate_request():
    """Створює нову заявку та додає її до черги."""
    global request_id
    request_id += 1
    request = f"Заявка №{request_id}"
    request_queue.put(request)
    print(f"[+] Створено: {request}")


def process_request():
    """Обробляє заявку з черги."""
    if not request_queue.empty():
        request = request_queue.get()
        print(f"[✓] Обробляється: {request}")
    else:
        print("[!] Черга порожня — немає що обробляти.")


def main():
    print("Система обробки заявок запущена. Натисніть Ctrl+C для виходу.\n")

    try:
        while True:
            # Імітація створення заявки (з випадковою паузою)
            if random.random() < 0.7:  # 70% ймовірність створення заявки
                generate_request()

            # Імітуємо обробку кожної ітерації
            process_request()

            time.sleep(1)  # пауза, щоб бачити процес у реальному часі

    except KeyboardInterrupt:
        print("\nПрограму зупинено користувачем.")


if __name__ == "__main__":
    main()
і