
file_path = r'D:\Project\vscode-basics\learning_neoversity\hw_neo\task_8_3.txt'


import re

def main(file_path: str):
    try:
        with open(file_path, 'r', encoding="utf-8") as file:    # відкриваємо файл у режимі читання у форматі utf-8
            log_list = []                                       # створюємо пустий список у який будеом додавати рядки з логів
            for line in file:
                log_list.append(parse_log_line(line))           # застосовуємо ф-цію, за результатом якої отримуємо список із значень і слів, який додаємо у список log_list, який створили раніше
            
            
            # print("Рівень логування | Кількість")
            # print("-----------------|----------")

            # for level, count in logs.items():
            #     print(f"{level:<16}| {count:<8}")
            
            
            
            
            
            
            
            
            
            
            print(filter_logs_by_level(log_list)) 
            print(log_list)
                    
    except:
        print("Файл не знайдено. Перевірте адресу або назву файлу.")
# parts[0], parts[1], parts[2], parts[3:] для розбора


def parse_log_line(line: str):
    # parts = line.replace('\n', '').split(' ') # потенційний рядок на видалення
    return line.replace('\n', '').split(' ') # отримумо рядок, у якому абзаци видаляємо шляхом заміни "абзацу" на "нічого", та розділюємо рядок за пробілами на окремі значення для списку


def filter_logs_by_level(log_list: list):               # ф-ція просто рахує кількість визначених значень у списку і повертає словником кількість INFO, DEBUG, ERROR, WARNING
    return {
        'INFO': sum('INFO' in entry for entry in log_list),
        'DEBUG': sum('DEBUG' in entry for entry in log_list),
        'ERROR': sum('ERROR' in entry for entry in log_list),
        'WARNING': sum('WARNING' in entry for entry in log_list)
    }



if __name__ == "__main__":
    main(file_path)
