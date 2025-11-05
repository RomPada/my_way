
import sys


def main(file_path: str, *args):
    try:

        with open(file_path, 'r', encoding="utf-8") as file:    # відкриваємо файл у режимі читання у форматі utf-8
            log_list = []                                       # створюємо пустий список у який будеом додавати рядки з логів
            for line in file:
                log_list.append(parse_log_line(line))           # застосовуємо ф-цію, за результатом якої отримуємо список із значень і слів, який додаємо у список log_list, який створили раніше
            print("Level of logs    | Amount")
            print("-----------------|----------")
            for level, count in filter_logs_by_level(log_list).items(): # за допомогою ф-ції друкуємо красивий результат зі словника
                print(f"{level:<17}| {count:<8}")
        
            if args:
                level_filter = args[0].upper()  # робимо нечутливим до регістру
                valid_levels = ("INFO", "DEBUG", "ERROR", "WARNING")

                if level_filter in valid_levels:
                    print(f"\nDetailed list of logs for the level {level_filter}:\n")
                    filtered_entries = [entry for entry in log_list if level_filter in entry]
                    if filtered_entries:
                        for entry in filtered_entries:
                            print(entry)
                    else:
                        print(f"\nThere are no entries for the level {level_filter}.")
                else:
                    print(f"\nUnknown level of log: {level_filter}. Available: {', '.join(valid_levels)}.")
            
    except:
        print("File not found. Check the address or file name..")



def parse_log_line(line: str):
    return line.replace('\n', '').split(' ')            # отримумо рядок, у якому абзаци видаляємо шляхом заміни "абзацу" на "нічого", та розділюємо рядок за пробілами на окремі значення для списку


def filter_logs_by_level(log_list: list):               # ф-ція просто рахує кількість визначених значень у списку і повертає словником кількість INFO, DEBUG, ERROR, WARNING
    return {
        'INFO': sum('INFO' in entry for entry in log_list),
        'DEBUG': sum('DEBUG' in entry for entry in log_list),
        'ERROR': sum('ERROR' in entry for entry in log_list),
        'WARNING': sum('WARNING' in entry for entry in log_list)
    }


if __name__ == "__main__":
    file_path = sys.argv[1]
    extra_args = sys.argv[2:]
    main(file_path, *extra_args)