# Імпортуємо UserDict. Це спеціальний клас, який дозволяє нам створити
# свій власний клас, що буде поводитися як стандартний словник Python (dict).
# Нам це потрібно для класу AddressBook.
from collections import UserDict

# --- Базовий клас для полів ---
# Це "батьківський" клас для всіх майбутніх полів, таких як Name, Phone, Email тощо.
# Він потрібен, щоб згрупувати спільну логіку.
class Field:
    # Конструктор класу. Це метод, який викликається автоматично
    # при створенні нового об'єкта (наприклад, Field("якесь значення")).
    def __init__(self, value):
        # Ми зберігаємо передане значення (value) усередині об'єкта
        # у "властивості" (атрибуті) з назвою self.value.
        self.value = value

    # "Магічний" метод __str__. Він визначає, що буде повертатися,
    # коли ми спробуємо "надрукувати" об'єкт (наприклад, print(my_field)).
    def __str__(self):
        # Просто повертаємо значення, яке зберігається, перетворене на рядок (string).
        return str(self.value)

# --- Клас для імені ---
# Цей клас "наслідує" (або "успадковує") поведінку від класу Field.
# Це означає, що він автоматично отримує все, що було у Field (value, __init__, __str__).
class Name(Field):
    # Ми "перевизначаємо" конструктор __init__, щоб додати свою логіку.
    def __init__(self, value: str):
        # value: str - це "підказка" (type hint), що ми очікуємо рядок.

        # str(value).strip() - 1) перетворюємо на рядок (про всяк випадок), 
        # 2) .strip() - видаляє зайві пробіли на початку та в кінці.
        value = str(value).strip()
        
        # Перевіряємо, чи не є ім'я порожнім рядком (наприклад, "" або " ") 
        # після того, як ми прибрали пробіли.
        if not value:
            # Якщо ім'я порожнє, ми "викидаємо" (raise) помилку ValueError.
            # Це зупинить виконання і повідомить, що щось пішло не так.
            raise ValueError("Name cannot be empty.")
        
        # super() - це спосіб звернутися до батьківського класу (у цьому випадку, Field).
        # super().__init__(value) - ми викликаємо "оригінальний" конструктор 
        # з класу Field і передаємо йому наше очищене та перевірене значення.
        super().__init__(value)

# --- Клас для телефону ---
# Цей клас також наслідує Field.
class Phone(Field):
    # Знову перевизначаємо конструктор, щоб додати валідацію (перевірку).
    def __init__(self, value: str):
        # Головна логіка валідації:
        # 1. len(value) != 10 - перевіряємо, чи довжина рядка НЕ дорівнює 10.
        # 2. not value.isdigit() - перевіряємо, чи рядок НЕ складається ТІЛЬКИ з цифр.
        #
        # Якщо хоча б одна з цих умов істинна (тому стоїть 'or' - "або"), 
        # то номер невалідний.
        if len(value) != 10 or not value.isdigit():
            # "Викидаємо" помилку з відповідним повідомленням.
            raise ValueError("Phone number must be 10 digits.")
        
        # Якщо обидві перевірки пройшли (тобто номер має 10 цифр),
        # ми викликаємо конструктор батьківського класу (Field), щоб зберегти це значення.
        super().__init__(value)

# --- Клас для Запису (один контакт) ---
# Цей клас об'єднує інформацію про ОДНОГО користувача:
# у нього є одне ім'я (Name) та список телефонів (list[Phone]).
class Record:
    # Конструктор класу. Приймає рядок з ім'ям.
    def __init__(self, name: str):
        # Ми не просто зберігаємо рядок 'name'. Ми створюємо об'єкт класу Name.
        # У цей момент відбувається валідація імені (перевірка на порожнечу у Name.__init__).
        self.name = Name(name)
        
        # Ми створюємо порожній список, який буде зберігати об'єкти класу Phone.
        # list[Phone] - це "підказка" (type hint), що у списку мають бути об'єкти Phone.
        self.phones: list[Phone] = []

    def add_phone(self, phone_number):
        """
        Запис контакту: ім'я + список телефонів.
        """
        # Ми не просто додаємо рядок. Ми створюємо об'єкт Phone(phone_number).
        # У цей момент відбувається валідація номера (перевірка на 10 цифр у Phone.__init__).
        # Якщо валідація не пройде, тут "викинеться" помилка, і додавання не відбудеться.
        # Якщо все добре, додаємо новий об'єкт Phone до нашого списку.
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number):
        """
        Видаляє телефон зі списку.
        """
        # Спочатку нам треба знайти *об'єкт* телефону, який відповідає рядку phone_number.
        # Для цього ми використовуємо інший наш метод - find_phone (описаний нижче).
        phone_to_remove = self.find_phone(phone_number)
        
        # find_phone поверне або об'єкт Phone, або None (якщо не знайде).
        if phone_to_remove:
            # Якщо щось знайшли, видаляємо цей об'єкт зі списку.
            self.phones.remove(phone_to_remove)
        else:
            # Якщо find_phone повернув None, значить такого номера немає.
            raise ValueError(f"Phone number {phone_number} not found.")

    def edit_phone(self, old_phone: str, new_phone: str):
        """
        Замінює старий телефон на новий.
        """
        # 1. Знаходимо *об'єкт*, який відповідає старому номеру.
        phone_to_edit = self.find_phone(old_phone)
        
        if phone_to_edit:
            # 2. Створюємо *новий об'єкт* Phone з нового номера.
            # Валідація нового номера (10 цифр) відбудеться тут.
            new_phone_obj = Phone(new_phone)
            
            # 3. Знаходимо індекс (порядковий номер) старого об'єкта у списку.
            index = self.phones.index(phone_to_edit)
            
            # 4. Замінюємо елемент у списку за цим індексом на новий об'єкт.
            self.phones[index] = new_phone_obj
        else:
            # Якщо старий номер не знайдено, "викидаємо" помилку.
            raise ValueError(f"Phone number {old_phone} not found.")

    def find_phone(self, phone_number: str):
        """
        Пошук телефону в записі. Повертає Phone або None..
        """
        # Проходимося по кожному *об'єкту* Phone у списку self.phones.
        for phone in self.phones:
            # Порівнюємо *значення* (phone.value) об'єкта з рядком, який шукаємо.
            if phone.value == phone_number:
                # Якщо знайшли - повертаємо *весь об'єкт* Phone.
                return phone
        
        # Якщо пройшли весь цикл і не знайшли, повертаємо None (означає "нічого").
        return None

    # "Магічний" метод, що визначає, як буде виглядати запис при print().
    def __str__(self):
        # f"...{}" - це f-рядок, зручний спосіб форматування.
        # 1. {self.name.value} - беремо наше ім'я (об'єкт Name) і його значення .value.
        # 2. {'; '.join(p.value for p in self.phones)} - це складніша частина:
        #    a. (p.value for p in self.phones) - "візьми .value для кожного об'єкта p у списку self.phones".
        #       (це називається "генератор", він створить щось на кшталт ['111', '222'])
        #    b. '; '.join(...) - "з'єднай усі елементи зі списку в один рядок, 
        #       вставляючи між ними '; '". (Результат: '111; 222')
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


# --- Клас для Адресної Книги ---
# Наслідується від UserDict. Це означає, що наш клас AddressBook
# автоматично отримує всю поведінку словника (dict).
# Всі дані будуть зберігатися у спеціальному атрибуті self.data (який є словником).
class AddressBook(UserDict):
    # Клас наслідується від UserDict, тому ми можемо 
    # використовувати self.data для зберігання записів (як у словнику)

    def add_record(self, record: Record):
        """
        Додає новий запис до self.data.
        Ключем є ім'я контакту (рядок), значенням - об'єкт Record.
        """
        # record: Record - підказка, що ми очікуємо об'єкт класу Record.
        
        # self.data - це наш "внутрішній" словник (який ми отримали від UserDict).
        # Ми додаємо новий елемент до словника:
        # Ключ: record.name.value (рядок, наприклад "John")
        # Значення: record (весь об'єкт Record для "John")
        self.data[record.name.value] = record

    def find(self, name):
        """
        Знаходить запис за ім'ям (ключем у self.data).
        """
        # .get(name) - це безпечний метод словника.
        # Він намагається знайти елемент за ключем 'name'.
        # Якщо знаходить - повертає значення (тобто *об'єкт Record*).
        # Якщо НЕ знаходить - повертає None (і не "викидає" помилку).
        return self.data.get(name)

    def delete(self, name):
        """
        Видаляє запис за ім'ям.
        """
        # .pop(name, None) - це безпечний метод видалення зі словника.
        # Він намагається видалити пару "ключ:значення" за ключем 'name'.
        # Якщо ключ існує - видаляє і повертає видалене значення (ми його не використовуємо).
        # Якщо ключ 'name' НЕ існує - він нічого не робить і повертає None (завдяки другому аргументу).
        # Це запобігає помилкам, якщо ми намагаємося видалити когось, кого немає у книзі.
        self.data.pop(name, None)



# # ----------------- Демонстрація (як у прикладі з умови) ----------------- GPT
# if __name__ == "__main__":
#     # Створення нової адресної книги
#     book = AddressBook()

#     # Створення запису для John
#     john_record = Record("John")
#     john_record.add_phone("1234567890")
#     john_record.add_phone("5555555555")

#     # Додавання запису John до адресної книги
#     book.add_record(john_record)

#     # Створення та додавання нового запису для Jane
#     jane_record = Record("Jane")
#     jane_record.add_phone("9876543210")
#     book.add_record(jane_record)

#     # Виведення всіх записів у книзі
#     for name, record in book.data.items():
#         print(record)

#     # Знаходження та редагування телефону для John
#     john = book.find("John")
#     john.edit_phone("1234567890", "1112223333")

#     print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

#     # Пошук конкретного телефону у записі John
#     found_phone = john.find_phone("5555555555")
#     print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

#     # Видалення запису Jane
#     book.delete("Jane")



# # --- Приклад використання --- GEMINI ---
# if __name__ == "__main__":
    
#     # Створення нової адресної книги
#     book = AddressBook()

#     # Створення запису для John
#     john_record = Record("John")
#     john_record.add_phone("1234567890")
#     john_record.add_phone("5555555555")

#     # Додавання запису John до адресної книги
#     book.add_record(john_record)

#     # Створення та додавання нового запису для Jane
#     jane_record = Record("Jane")
#     jane_record.add_phone("9876543210")
#     book.add_record(jane_record)

#     # Виведення всіх записів у книзі
#     print("--- All contacts ---")
#     for name, record in book.data.items():
#         print(record)
#     print("----------------------")

#     # Знаходження та редагування телефону для John
#     john = book.find("John")
#     john.edit_phone("1234567890", "1112223333")

#     print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

#     # Пошук конкретного телефону в записі John
#     found_phone = john.find_phone("5555555555")
#     print(f"** find_phone    {john.name}: {found_phone}")  # Виведення: John: 5555555555


#     # Видалення запису Jane
    
#     book.delete("Jane")

#     # Перевірка, що Jane видалена
#     print("--- Contacts after deletion ---")
#     for name, record in book.data.items():
#         print(record)
#     print("-------------------------------")
    
#     # Приклад валідації (спробуємо додати невірний номер)
#     try:
#         john_record.add_phone("123")
#     except ValueError as e:
#         print(f"Validation error: {e}")
