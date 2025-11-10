import functools
from collections import UserDict
from datetime import datetime, timedelta


def input_error(func):
    """
    Декоратор для обробки помилок вводу.
    """
    @functools.wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError as e:
            return f"Key error: {e}"
        except IndexError:
            return "Not enough arguments. Please print full info."
        except Exception as e:
            return f"Error: {e}"
    return inner


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value: str):
        value = str(value).strip()
        if not value:
            raise ValueError("Name cannot be empty.")
        super().__init__(value)

class Phone(Field):
    def __init__(self, value: str):
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Phone number must be 10 numerics.")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value: str):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday: Birthday = None

    def add_phone(self, phone_number: str):
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number: str):
        phone_to_remove = self.find_phone(phone_number)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
        else:
            raise ValueError(f"Phone number {phone_number} not found.")

    def edit_phone(self, old_phone: str, new_phone: str):
        phone_to_edit = self.find_phone(old_phone)
        if phone_to_edit:
            new_phone_obj = Phone(new_phone)
            index = self.phones.index(phone_to_edit)
            self.phones[index] = new_phone_obj
        else:
            raise ValueError(f"Phone number {old_phone} not found.")

    def find_phone(self, phone_number: str):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def add_birthday(self, birthday_str: str):
        """
        Додає день народження до запису.
        Валідація відбувається в класі Birthday.
        """
        self.birthday = Birthday(birthday_str)

    def __str__(self):
        phones_str = '; '.join(p.value for p in self.phones)
        birthday_str = ""
        if self.birthday:
            birthday_str = f", birthday: {self.birthday.value.strftime('%d.%m.%Y')}"
        return f"Contact name: {self.name.value}, phones: {phones_str}{birthday_str}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str) -> Record:
        return self.data.get(name)

    def delete(self, name: str):
        self.data.pop(name, None)

    def get_upcoming_birthdays(self) -> list:
        upcoming_birthdays = []
        today = datetime.today().date()
        for user in self.data.values():
            if user.birthday:
                try:
                    birthday = user.birthday.value.date() 
                    birthday_this_year = birthday.replace(year=today.year)
                    if birthday_this_year < today:
                        birthday_this_year = birthday_this_year.replace(year=today.year + 1)
                    diff = (birthday_this_year - today).days
                    if 0 <= diff <= 7:
                        if birthday_this_year.weekday() == 5: # Субота
                            birthday_this_year += timedelta(days=2)
                        elif birthday_this_year.weekday() == 6: # Неділя
                            birthday_this_year += timedelta(days=1)
                        congratulation_date_str = birthday_this_year.strftime("%d.%m.%Y")
                        upcoming_birthdays.append(
                            {"name": user.name.value, "congratulation_date": congratulation_date_str}
                        )
                except Exception as e:
                    print(f"Error processing {user.name.value}: {e}")

        return upcoming_birthdays


def parse_input(user_input):
    """
    Розбирає введений рядок на команду та аргументи.
    """
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book: AddressBook):
    """
    Додає контакт або новий телефон до існуючого контакту.
    Викликає помилку, якщо телефон не 10 цифр.
    """
    name, phone = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    record.add_phone(phone)
    return message


@input_error
def change_contact(args, book: AddressBook):
    """
    Змінює існуючий телефон на новий.
    Викликає помилку, якщо контакт не знайдено, 
    старий телефон не знайдено, або новий телефон не 10 цифр.
    """
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Contact changed."
    else:
        raise KeyError


@input_error
def show_phone(args, book: AddressBook):
    """
    Показує всі телефони вказаного контакту.
    """
    name = args[0]
    record = book.find(name)
    if record:
        return '; '.join(p.value for p in record.phones)
    else:
        raise KeyError


def show_all(book: AddressBook):
    """
    Показує всі контакти в адресній книзі.
    """
    if not book.data:
        return "List is empty."
    
    return "\n".join(str(record) for record in book.data.values())


@input_error
def add_birthday(args, book: AddressBook):
    """
    Додає день народження до контакту.
    Викликає помилку, якщо формат дати DD.MM.YYYY.
    """
    name, birthday_str = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday_str)
        return "Birthday added."
    else:
        raise KeyError


@input_error
def show_birthday(args, book: AddressBook):
    """
    Показує день народження контакту.
    """
    name = args[0]
    record = book.find(name)
    if record:
        if record.birthday:
            return record.birthday.value.strftime("%d.%m.%Y")
        else:
            return "Birthday not set for this contact."
    else:
        raise KeyError


def birthdays(book: AddressBook):
    """
    Показує дні народження на наступний тиждень.
    """
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays in the next week."
    result = ["Upcoming birthdays:"]
    for item in upcoming:
        result.append(f"  {item['name']}: {item['congratulation_date']}")
    return "\n".join(result)


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    print("Type 'hello' for a greeting or 'help' for commands.")

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command in ["hello", "hi"]:
            print("How can I help you?")
            
        elif command == "help":
            print("Available commands:")
            print("  add [name] [phone]         - Add a new contact or phone")
            print("  change [name] [old] [new]  - Change a phone number")
            print("  phone [name]               - Show phones for a contact")
            print("  all                        - Show all contacts")
            print("  add-birthday [name] [date] - Add birthday (DD.MM.YYYY)")
            print("  show-birthday [name]       - Show a contact's birthday")
            print("  birthdays                  - Show upcoming birthdays")
            print("  close / exit               - Exit the bot")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(book))

        else:
            print("Invalid command. Type 'help' for a list of commands.")


if __name__ == "__main__":
    main()
