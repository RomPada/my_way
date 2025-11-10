from __future__ import annotations
from collections import UserDict
from datetime import datetime, date, timedelta
from typing import Optional, List, Dict, Tuple, Callable


# ---------- СЕРВІС: декоратор для дружніх помилок ----------
def input_error(func: Callable):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"Value error: {e}"
        except KeyError as e:
            return f"Key error: {e}"
        except IndexError:
            return "Not enough arguments."
        except Exception as e:
            return f"Error: {e}"
    return wrapper


# ---------- МОДЕЛІ ДАНИХ ----------
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
        value = str(value).strip()
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Phone number must be 10 digits.")
        super().__init__(value)


class Birthday(Field):
    """
    Зберігаємо як date. Приймаємо тільки формат DD.MM.YYYY.
    """
    def __init__(self, value: str):
        value = str(value).strip()
        try:
            dt = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(dt)

    def __str__(self) -> str:
        return self.value.strftime("%d.%m.%Y")


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: List[Phone] = []
        self.birthday: Optional[Birthday] = None

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

    def find_phone(self, phone_number: str) -> Optional[Phone]:
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def add_birthday(self, date_str: str):
        """
        Додає або оновлює день народження (валідація всередині Birthday).
        """
        self.birthday = Birthday(date_str)

    def __str__(self):
        phones_str = "; ".join(p.value for p in self.phones) if self.phones else "—"
        bday_str = str(self.birthday) if self.birthday else "—"
        return f"Contact name: {self.name.value}, phones: {phones_str}, birthday: {bday_str}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str) -> Optional[Record]:
        return self.data.get(name)

    def delete(self, name: str):
        self.data.pop(name, None)

    # --- Головна логіка для ДН на наступний тиждень ---
    def get_upcoming_birthdays(self, today: Optional[date] = None) -> List[Tuple[str, date]]:
        """
        Повертає список (name, congratulation_date) для тих, кого треба привітати
        протягом наступного тижня (з понеділка по неділю наступного тижня).
        Якщо ДН припадає на вихідні, привітання переноситься на понеділок.
        """
        if today is None:
            today = date.today()

        # Знайдемо понеділок наступного тижня
        # День тижня: понеділок=0 ... неділя=6
        days_to_next_monday = (7 - today.weekday()) % 7
        if days_to_next_monday == 0:
            days_to_next_monday = 7  # якщо сьогодні понеділок — наступний понеділок через 7 днів
        next_monday = today + timedelta(days=days_to_next_monday)
        next_sunday = next_monday + timedelta(days=6)

        result: List[Tuple[str, date]] = []

        for record in self.data.values():
            if not record.birthday:
                continue

            # ДН цього року або наступного, якщо вже минув
            bday_this_year = record.birthday.value.replace(year=next_monday.year)
            if bday_this_year < next_monday:
                # можливо, ДН був на поч. року, а ми вже у грудні і "наступний тиждень" у наступному році
                bday_this_year = record.birthday.value.replace(year=next_monday.year + 1)

            # Якщо дата ДН потрапляє у вікно наступного тижня
            if next_monday <= bday_this_year <= next_sunday:
                congr_date = bday_this_year
                # Перенесення з вихідних на понеділок
                if congr_date.weekday() == 5:       # субота
                    congr_date = congr_date + timedelta(days=2)
                elif congr_date.weekday() == 6:     # неділя
                    congr_date = congr_date + timedelta(days=1)
                result.append((record.name.value, congr_date))

        # Відсортуємо за датою привітання, потім за ім'ям
        result.sort(key=lambda x: (x[1], x[0]))
        return result


# ---------- ПАРСИНГ КОМАНД ----------
def parse_input(user_input: str):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


# ---------- ОБРОБНИКИ КОМАНД ----------
@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_phone(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact '{name}' not found.")
    record.edit_phone(old_phone, new_phone)
    return "Phone changed."


@input_error
def show_contact(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record is None:
        return f"Contact {name} not found."
    phones = "; ".join(p.value for p in record.phones) if record.phones else "—"
    bday = str(record.birthday) if record.birthday else "—"
    return f"{name}: {phones} | birthday: {bday}"


def all_contacts(book: AddressBook):
    if not book.data:
        return "List is empty."
    lines = ["All contacts:"]
    for record in book.data.values():
        lines.append(f"  {record}")
    return "\n".join(lines)


@input_error
def add_birthday(args, book: AddressBook):
    name, date_str, *_ = args
    record = book.find(name)
    if record is None:
        # Дозволимо одразу створити контакт із ДН
        record = Record(name)
        book.add_record(record)
        created = True
    else:
        created = False
    record.add_birthday(date_str)  # валідація всередині
    return "Birthday added." if created else "Birthday updated."


@input_error
def show_birthday(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record is None:
        return f"Contact {name} not found."
    if not record.birthday:
        return f"{name} has no birthday set."
    return f"{name}: {record.birthday}"


@input_error
def birthdays(args, book: AddressBook):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No birthdays next week."
    # Групування за датами для зручності
    by_date: Dict[date, List[str]] = {}
    for name, d in upcoming:
        by_date.setdefault(d, []).append(name)

    lines = ["Birthdays next week:"]
    for d in sorted(by_date.keys()):
        names = ", ".join(sorted(by_date[d]))
        lines.append(f"  {d.strftime('%d.%m.%Y')} (Mon-Sun window): {names}")
    return "\n".join(lines)


# ---------- ГОЛОВНИЙ ЦИКЛ ----------
def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    print("Print 'help' for all commands.")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command in ["hello", "hi"]:
            print("How can I help you?")

        elif command == "help":
            print(
                "Commands:\n"
                "  add <name> <phone>\n"
                "  change <name> <old phone> <new phone>\n"
                "  phone <name>\n"
                "  all\n"
                "  add-birthday <name> <DD.MM.YYYY>\n"
                "  show-birthday <name>\n"
                "  birthdays\n"
                "  exit | close"
            )

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_phone(args, book))

        elif command == "phone":
            print(show_contact(args, book))

        elif command == "all":
            print(all_contacts(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
