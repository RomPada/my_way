import functools
import pickle
import re
from collections import UserDict
from datetime import datetime, timedelta

# -----------------------------------------------------------------------------
# 1. ДЕКОРАТОР ОБРОБКИ ПОМИЛОК
# (Виправлено невелику одруківку 'e:a' -> 'e:')
# -----------------------------------------------------------------------------

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
            # Використовуємо кастомне повідомлення, якщо воно є
            if str(e):
                return str(e)
            return "Key error (contact not found or note ID invalid)."
        except IndexError:
            return "Недостатньо аргументів. Будь ласка, введіть повну команду."
        except Exception as e:
            return f"Error: {e}"
    return inner

# -----------------------------------------------------------------------------
# 2. КЛАСИ ПОЛІВ (Field) ТА ЗАПИСУ (Record)
# (Додано Email, Address та відповідні методи в Record)
# -----------------------------------------------------------------------------

class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    def __str__(self):
        return str(self.value)

class Name(Field):
    @Field.value.setter
    def value(self, new_value: str):
        new_value = str(new_value).strip()
        if not new_value:
            raise ValueError("Name cannot be empty.")
        self._value = new_value

class Phone(Field):
    @Field.value.setter
    def value(self, new_value: str):
        if len(new_value) != 10 or not new_value.isdigit():
            raise ValueError("Phone number must be 10 numerics.")
        self._value = new_value

class Birthday(Field):
    @Field.value.setter
    def value(self, new_value: str):
        try:
            self._value = datetime.strptime(new_value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")

class Email(Field):
    @Field.value.setter
    def value(self, new_value: str):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", new_value):
            raise ValueError("Invalid email format.")
        self._value = new_value

class Address(Field):
    @Field.value.setter
    def value(self, new_value: str):
        if not new_value:
            raise ValueError("Address cannot be empty.")
        self._value = new_value

class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday: Birthday = None
        self.email: Email = None
        self.address: Address = None

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
            phone_to_edit.value = new_phone # Використовуємо setter
        else:
            raise ValueError(f"Phone number {old_phone} not found.")

    def find_phone(self, phone_number: str):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def add_birthday(self, birthday_str: str):
        self.birthday = Birthday(birthday_str)

    def add_email(self, email_str: str):
        self.email = Email(email_str)

    def add_address(self, address_str: str):
        self.address = Address(address_str)

    def __str__(self):
        phones_str = '; '.join(p.value for p in self.phones)
        birthday_str = f", birthday: {self.birthday}" if self.birthday else ""
        email_str = f", email: {self.email}" if self.email else ""
        address_str = f", address: {self.address}" if self.address else ""
        return (f"Contact name: {self.name.value}, phones: {phones_str}"
                f"{email_str}{address_str}{birthday_str}")

# -----------------------------------------------------------------------------
# 3. КЛАС АДРЕСНОЇ КНИГИ (AddressBook)
# (Додано search, змінено get_upcoming_birthdays)
# -----------------------------------------------------------------------------

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str) -> Record:
        return self.data.get(name)

    def delete(self, name: str):
        if not self.data.pop(name, None):
            raise KeyError(f"Contact {name} not found.")

    def search(self, query: str) -> list:
        """Пошук за будь-яким збігом у імені, телефоні або email."""
        query = query.lower()
        results = []
        for record in self.data.values():
            if query in record.name.value.lower():
                results.append(str(record))
                continue
            if any(query in phone.value for phone in record.phones):
                results.append(str(record))
                continue
            if record.email and query in record.email.value.lower():
                results.append(str(record))
                continue
        return results

    def get_upcoming_birthdays(self, days_ahead: int = 7) -> list:
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
                    
                    if 0 <= diff <= days_ahead:
                        # Логіка перенесення на понеділок, якщо СБ або НД
                        weekday = birthday_this_year.weekday()
                        if weekday == 5: # Субота
                            congratulation_date = birthday_this_year + timedelta(days=2)
                        elif weekday == 6: # Неділя
                            congratulation_date = birthday_this_year + timedelta(days=1)
                        else:
                            congratulation_date = birthday_this_year
                            
                        congratulation_date_str = congratulation_date.strftime("%d.%m.%Y")
                        upcoming_birthdays.append(
                            {"name": user.name.value, "congratulation_date": congratulation_date_str}
                        )
                except Exception as e:
                    print(f"Error processing {user.name.value}: {e}")

        return upcoming_birthdays

# -----------------------------------------------------------------------------
# 4. СИСТЕМА НОТАТОК (NoteBook) - НОВИЙ ФУНКЦІОНАЛ
# (Включаючи розширений функціонал з тегами)
# -----------------------------------------------------------------------------

class Tag(Field):
    @Field.value.setter
    def value(self, new_value: str):
        self._value = str(new_value).lower().strip()

class Note:
    def __init__(self, content: str):
        if not content:
            raise ValueError("Note content cannot be empty.")
        self.content = content
        self.tags: list[Tag] = []

    def add_tag(self, tag_str: str):
        tag = Tag(tag_str)
        if tag.value and tag.value not in [t.value for t in self.tags]:
            self.tags.append(tag)

    def __str__(self):
        tags_str = f" [Tags: {', '.join(t.value for t in self.tags)}]" if self.tags else ""
        return f"Note: {self.content}{tags_str}"

class NoteBook(UserDict):
    def __init__(self):
        super().__init__()
        self.next_id = 1

    def add_note(self, note: Note):
        self.data[self.next_id] = note
        current_id = self.next_id
        self.next_id += 1
        return f"Note {current_id} added."

    def find_by_id(self, note_id: int) -> Note:
        note = self.data.get(note_id)
        if not note:
            raise KeyError("Note ID not found.")
        return note

    def delete_note(self, note_id: int):
        if self.data.pop(note_id, None):
            return "Note deleted."
        raise KeyError("Note ID not found.")

    def edit_note(self, note_id: int, new_content: str):
        note = self.find_by_id(note_id)
        note.content = new_content
        return "Note updated."
    
    def add_tag_to_note(self, note_id: int, tag_str: str):
        note = self.find_by_id(note_id)
        note.add_tag(tag_str)
        return "Tag added."

    def search_by_content(self, query: str) -> list:
        query = query.lower()
        return [f"ID {id}: {note}" for id, note in self.data.items() if query in note.content.lower()]

    def search_by_tag(self, tag_query: str) -> list:
        tag_query = tag_query.lower()
        results = []
        for id, note in self.data.items():
            if any(tag_query == tag.value for tag in note.tags):
                results.append(f"ID {id}: {note}")
        return results

    def __str__(self):
        if not self.data:
            return "Note book is empty."
        return "\n".join(f"ID {id}: {note}" for id, note in self.data.items())

# -----------------------------------------------------------------------------
# 5. ФУНКЦІЇ ЗБЕРЕЖЕННЯ/ЗАВАНТАЖЕННЯ (НОВИЙ ФУНКЦІОНАЛ)
# -----------------------------------------------------------------------------

def save_data(data, filename="data.pkl"):
    """Зберігає обидві книги у файл."""
    with open(filename, "wb") as f:
        pickle.dump(data, f)

def load_data(filename="data.pkl"):
    """Завантажує дані. Якщо файл не знайдено, повертає нові книги."""
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError):
        return {"address_book": AddressBook(), "note_book": NoteBook()}

# -----------------------------------------------------------------------------
# 6. ФУНКЦІЇ ОБРОБКИ КОМАНД
# -----------------------------------------------------------------------------

def parse_input(user_input):
    """
    Розбирає введений рядок на команду та аргументи.
    """
    parts = user_input.split()
    cmd = parts[0].strip().lower()
    args = parts[1:]
    return cmd, args

# --- Команди адресної книги ---

@input_error
def add_contact(args, book: AddressBook):
    """
    Додає контакт або новий телефон до існуючого контакту.
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
    """
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Contact changed."
    else:
        raise KeyError(f"Contact {name} not found.")

@input_error
def show_phone(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record:
        if not record.phones:
            return "No phones set for this contact."
        return '; '.join(p.value for p in record.phones)
    else:
        raise KeyError(f"Contact {name} not found.")

def show_all(book: AddressBook):
    if not book.data:
        return "List is empty."
    return "\n".join(str(record) for record in book.data.values())

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday_str = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday_str)
        return "Birthday added."
    else:
        raise KeyError(f"Contact {name} not found.")

@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record:
        if record.birthday:
            return str(record.birthday)
        else:
            return "Birthday not set for this contact."
    else:
        raise KeyError(f"Contact {name} not found.")

@input_error
def birthdays(args, book: AddressBook):
    """
    Показує дні народження. 
    Приймає опціональний аргумент [days]. За замовчуванням 7.
    """
    days_ahead = 7
    if args:
        try:
            days_ahead = int(args[0])
        except ValueError:
            return "Please enter a valid number of days."
            
    upcoming = book.get_upcoming_birthdays(days_ahead)
    if not upcoming:
        return f"No upcoming birthdays in the next {days_ahead} days."
    result = [f"Upcoming birthdays in the next {days_ahead} days:"]
    for item in upcoming:
        result.append(f"  {item['name']}: {item['congratulation_date']}")
    return "\n".join(result)

# --- НОВІ команди адресної книги ---

@input_error
def add_email(args, book: AddressBook):
    name, email = args
    record = book.find(name)
    if record:
        record.add_email(email)
        return "Email added."
    else:
        raise KeyError(f"Contact {name} not found.")

@input_error
def add_address(args, book: AddressBook):
    name, *address_parts = args
    if not address_parts:
        raise ValueError("Address cannot be empty.")
    address = " ".join(address_parts)
    record = book.find(name)
    if record:
        record.add_address(address)
        return "Address added."
    else:
        raise KeyError(f"Contact {name} not found.")

@input_error
def search_contacts(args, book: AddressBook):
    query = args[0]
    results = book.search(query)
    if not results:
        return "No matches found."
    return "\n".join(results)

@input_error
def delete_contact(args, book: AddressBook):
    name = args[0]
    book.delete(name)
    return "Contact deleted."

# --- НОВІ команди для нотаток ---

@input_error
def add_note(args, n_book: NoteBook):
    content = " ".join(args)
    note = Note(content)
    return n_book.add_note(note)

def show_all_notes(n_book: NoteBook):
    return str(n_book)

@input_error
def edit_note(args, n_book: NoteBook):
    note_id = int(args[0])
    new_content = " ".join(args[1:])
    if not new_content:
        raise ValueError("Note content cannot be empty.")
    return n_book.edit_note(note_id, new_content)

@input_error
def delete_note(args, n_book: NoteBook):
    note_id = int(args[0])
    return n_book.delete_note(note_id)

@input_error
def add_tag(args, n_book: NoteBook):
    note_id = int(args[0])
    tag = args[1]
    return n_book.add_tag_to_note(note_id, tag)

@input_error
def search_notes(args, n_book: NoteBook):
    query = " ".join(args)
    results = n_book.search_by_content(query)
    if not results:
        return "No notes found matching this content."
    return "\n".join(results)

@input_error
def search_tag(args, n_book: NoteBook):
    tag_query = args[0]
    results = n_book.search_by_tag(tag_query)
    if not results:
        return "No notes found with this tag."
    return "\n".join(results)

# -----------------------------------------------------------------------------
# 7. ГОЛОВНА ФУНКЦІЯ (main)
# (Оновлена для завантаження/збереження та нових команд)
# -----------------------------------------------------------------------------

def main():
    # Завантажуємо дані при старті
    data = load_data()
    book: AddressBook = data["address_book"]
    n_book: NoteBook = data["note_book"]
    
    print("gggggg Welcome to the personal assistant! gggggg")
    print("Type 'help' for commands.")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)
        
        data_changed = False # Прапорець, що дані змінились

        if command in ["close", "exit"]:
            if data_changed: # Зберігаємо, лише якщо були зміни (оптимізація)
                save_data({"address_book": book, "note_book": n_book})
            print("Good bye!")
            break

        elif command in ["hello", "hi"]:
            print("How can I help you?")
            
        elif command == "help":
            print("--- Contact Commands ---")
            print("  add [name] [phone]             - Add a new contact or phone")
            print("  change [name] [old] [new]      - Change a phone number")
            print("  phone [name]                   - Show phones for a contact")
            print("  add-birthday [name] [date]     - Add birthday (DD.MM.YYYY)")
            print("  show-birthday [name]           - Show a contact's birthday")
            print("  add-email [name] [email]       - Add an email")
            print("  add-address [name] [address]   - Add an address")
            print("  delete [name]                  - Delete a contact")
            print("  all                            - Show all contacts")
            print("  search [query]                 - Search contacts (by name, phone, email)")
            print("  birthdays [days]               - Show upcoming birthdays (default 7 days)")
            print("--- Note Commands ---")
            print("  add-note [content]             - Add a new note")
            print("  all-notes                      - Show all notes")
            print("  edit-note [ID] [new content]   - Edit a note by its ID")
            print("  delete-note [ID]               - Delete a note by its ID")
            print("  add-tag [ID] [tag]             - Add a tag to a note by ID")
            print("  search-notes [query]           - Search notes by content")
            print("  search-tag [tag]               - Search notes by tag")
            print("--- General Commands ---")
            print("  close / exit                   - Exit the bot")

        # --- Contact Commands ---
        elif command == "add":
            print(add_contact(args, book))
            data_changed = True
        elif command == "change":
            print(change_contact(args, book))
            data_changed = True
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
            data_changed = True
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        elif command == "add-email":
            print(add_email(args, book))
            data_changed = True
        elif command == "add-address":
            print(add_address(args, book))
            data_changed = True
        elif command == "search":
            print(search_contacts(args, book))
        elif command == "delete":
            print(delete_contact(args, book))
            data_changed = True

        # --- Note Commands ---
        elif command == "add-note":
            print(add_note(args, n_book))
            data_changed = True
        elif command == "all-notes":
            print(show_all_notes(n_book))
        elif command == "edit-note":
            print(edit_note(args, n_book))
            data_changed = True
        elif command == "delete-note":
            print(delete_note(args, n_book))
            data_changed = True
        elif command == "add-tag":
            print(add_tag(args, n_book))
            data_changed = True
        elif command == "search-notes":
            print(search_notes(args, n_book))
        elif command == "search-tag":
            print(search_tag(args, n_book))

        else:
            print("Invalid command. Type 'help' for a list of commands.")

        # Авто-збереження після кожної успішної зміни
        if data_changed:
            save_data({"address_book": book, "note_book": n_book})


if __name__ == "__main__":
    main()