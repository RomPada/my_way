
path = r'D:\Project\vscode-basics\learning_neoversity\hw_neo\task_6_2.txt'

def get_cats_info(path):
    try:
        with open(path, 'r', encoding="utf-8") as file:
            cats_info = []
            for cat_line in file:
                cat_list = cat_line.replace('\n', '').split(',')
                key_list = ["id", "name", "age"]
                cat_dict = dict(zip(key_list, cat_list))
                cats_info.append(cat_dict)
            print(cats_info)
        return cats_info
    except:
        print("Помилка.")

get_cats_info(path)
