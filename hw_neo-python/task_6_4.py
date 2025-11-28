
def parse_input(user_input):
    cmd, *args = user_input.split() # приймає рядок вводу користувача user_input і розбиває його на слова за допомогою методу split(). Вона повертає перше слово як команду cmd та решту як список аргументів *args.
    cmd = cmd.strip().lower() # розділяє рядок на слова. Перше слово зберігається у змінній cmd, а решта зберігається у списку args завдяки оператору розпакування *. Далі рядок коду cmd = cmd.strip().lower() видаляє зайві пробіли навколо команди та перетворює її на нижній регістр.
    return cmd, *args

def add_contact(args, contacts):
    name, phone = args # два елементи зі списку args розпаковуються в змінні name та phone
    if name in contacts: 
        return f"{name} is already listed."
    else:
        contacts[name] = phone # додає пару "ключ: значення" до словника контактів, використовуючи ім'я як ключ і телефонний номер як значення contacts[name] = phone.
        return "Contact added."
    
def show_contact(args, contacts):
    name = args[0]
    if name in contacts:
        return f"{name}: {contacts[name]}"
    else:
        return f"Contact {name} not found."
    
def all_contacts(contacts):
    if contacts:
        result = "All contacts:\n"
        for name, phone in contacts.items(): # Метод .items() повертає пари ключ–значення у вигляді: Цикл for проходиться по кожній парі - у змінну name потрапляє ключ (ім’я контакта), у змінну phone — значення (номер телефона).
            result += f"  {name}: {phone}\n" # \n означає перенос рядка. Оператор += додає цей текст до змінної result.
        return result.strip()
    else:
        return "List is empty."

def change_phone(args, contacts):
    name, phone = args
    contacts[name] = phone
    return "Contact changed."

def main():
    contacts = {}
    print("Welcome to the assistant bot!")
    print("Print 'help' for all commands.")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input) # результат функції parse_input() повертає кілька значень (наприклад, список або кортеж), і ми розкладаємо ці значення на дві частини: перше — це command, решта — у список args.
        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command in ["hello", "hi"]:
            print("How can I help you?")
        elif command == "help":
            print("Commands: add <name> <phone>, change <username> <new phone>, show <name>, all, exit (close)")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "phone":
            print(show_contact(args, contacts))
        elif command == "all":
            print(all_contacts(contacts))
        elif command == "change":
            print(change_phone(args, contacts))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
