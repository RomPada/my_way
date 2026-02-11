
path = r'D:\Project\vscode-basics\learning_neoversity\hw_neo\task_6_1.txt'

import re

def total_salary(path):
    try:
        with open(path, 'r', encoding="utf-8") as file:
            file_readed = file.readlines()
            file_strn = str(file_readed)
            #import re
            numbers_list = [int(x) for x in re.findall(r'\d+', file_strn)]
            len_list = len(numbers_list)
            total = sum(numbers_list)
            average = int(total / len_list)
            result = (total, average)
            print(f"Загальна сума заробітної плати: {total}, Середня заробітна плата: {average}.")
        return result
    except:
        print("Файл не знайдено. Перевірте адресу або назву файлу.")

total_salary(path)
