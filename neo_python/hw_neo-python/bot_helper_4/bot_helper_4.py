import functools
import json
import re
from collections import UserDict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict

# =========================
# Константи збереження
# =========================
APP_DIR = Path.home() / ".assistant_data"
CONTACTS_PATH = APP_DIR / "contacts.json"
NOTES_PATH = APP_DIR / "notes.json"
DATE_FMT = "%d.%m.%Y"


# =========================
# Декоратор обробки помилок
# =========================
def input_error(func):
    """
    Простий декоратор: ловимо популярні помилки і
    повертаємо дружнє повідомлення замість трейсбеку.
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


# =========================
# Поля і валідація
# =========================
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
        value = value.strip()
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Phone number must be 10 numerics.")
        super().__init__(value)


class Email(Field):
    EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$")

    def __init__(self, value: str):
        value = value.strip()
        if value and not Email.EMAIL_RE.match(value):
            raise ValueError("Invalid email format.")
        super().__init__(value)


class Address(Field):
    def __init__(self, value: str):
        super().__init__(value.strip())


class Birthday(Field):
    def __init__(self, value: str):
        value = value.strip()
        try:
            self.value = datetime.strptime(value, DATE_FMT)
        except ValueError:
            raise ValueError(f"Invalid date format. Use {DATE_FMT}")


# =========================
# Модель запису контакту
# =========================
class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: List[Phone] = []
        self.email: Optional[Email] = None
        self.address: Optional[Address] = None
        self.birthday: Optional[Birthday] = None

    # ---- Телефони
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
            idx = self.phones.index(phone_to_edit)
            self.phones[idx] = new_phone_obj
        else:
            raise ValueError(f"Phone number {old_phone} not found.")

    def find_phone(self, phone_number: str):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    # ---- Email / Address / Birthday
    def set_email(self, email_str: str):
        self.email = Email(email_str)

    def set_address(self, address_str: str):
        self.address = Address(address_str)

    def set_birthday(self, birthday_str: str):
        self.birthday = Birthday(birthday_str)

    def to_dict(self) -> Dict:
        return {
            "name": self.name.value,
            "phones": [p.value for p in self.phones],
            "email": self.email.value if self.email else "",
            "address": self.address.value if self.address else "",
            "birthday": self.birthday.value.strftime(DATE_FMT) if self.birthday else ""
        }

    @staticmethod
    def from_dict(data: Dict) -> "Record":
        rec = Record(data["name"])
        for ph in data.get("phones", []):
            rec.add_phone(ph)
        if data.get("email"):
            rec.set_email(data["email"])
        if data.get("address"):
            rec.set_address(data["address"])
        if data.get("birthday"):
            rec.set_birthday(data["birthday"])
        return rec

    def __str__(self):
        phones_str = "; ".join(p.value for p in self.phones) if self.phones else "-"
        email_str = self.email.value if self.email and self.email.value else "-"
        addr_str = self.address.value if self.address and self.address.value else "-"
        bday_str = self.birthday.value.strftime(DATE_FMT) if self.birthday else "-"
        return (f"{self.name.value:20} | phones: {phones_str:15} | "
                f"email: {email_str:25} | addr: {addr_str:20} | bday: {bday_str}")


# =========================
# Книга контактів з пошуком і ДН
# =========================
class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value.lower()] = record

    def find(self, name: str) -> Optional[Record]:
        return self.data.get(name.lower())

    def delete(self, name: str):
        self.data.pop(name.lower(), None)

    def search(self, query: str) -> List[Record]:
        """
        Простий пошук по імені/телефонах/email/адресі (регістр ігнорується).
        """
        q = query.lower()
        res = []
        for rec in self.data.values():
            if q in rec.name.value.lower():
                res.append(rec)
                continue
            if any(q in p.value for p in rec.phones):
                res.append(rec)
                continue
            if rec.email and q in rec.email.value.lower():
                res.append(rec)
                continue
            if rec.address and q in rec.address.value.lower():
                res.append(rec)
                continue
        return res

    def birthdays_in(self, days: int) -> List[Dict[str, str]]:
        """
        Список ДН у найближчі N днів (переносимо привітання з вихідних на понеділок).
        """
        upcoming = []
        today = datetime.today().date()
        for user in self.data.values():
            if not user.birthday:
                continue
            try:
                bday = user.birthday.value.date()
                this_year = bday.replace(year=today.year)
                if this_year < today:
                    this_year = this_year.replace(year=today.year + 1)
                diff = (this_year - today).days
                if 0 <= diff <= days:
                    # Перенос на робочий день
                    if this_year.weekday() == 5:  # Субота
                        this_year += timedelta(days=2)
                    elif this_year.weekday() == 6:  # Неділя
                        this_year += timedelta(days=1)
                    upcoming.append({
                        "name": user.name.value,
                        "congratulation_date": this_year.strftime(DATE_FMT)
                    })
            except Exception as e:
                print(f"Error processing {user.name.value}: {e}")
        return upcoming

    # ---- Збереження / завантаження
    def to_list(self) -> List[Dict]:
        return [rec.to_dict() for rec in self.data.values()]

    @staticmethod
    def from_list(items: List[Dict]) -> "AddressBook":
        book = AddressBook()
        for d in items:
            book.add_record(Record.from_dict(d))
        return book


# =========================
# Нотатки з тегами
# =========================
class Note:
    def __init__(self, text: str, tags: Optional[List[str]] = None):
        self.text = text.strip()
        self.tags = sorted({t.strip().lower() for t in (tags or []) if t.strip()})
        self.created_at = datetime.now()

    def to_dict(self) -> Dict:
        return {
            "text": self.text,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(timespec="seconds")
        }

    @staticmethod
    def from_dict(d: Dict) -> "Note":
        n = Note(d.get("text", ""), d.get("tags", []))
        try:
            n.created_at = datetime.fromisoformat(d.get("created_at"))
        except Exception:
            pass
        return n

    def __str__(self):
        tags = ", ".join(self.tags) if self.tags else "-"
        created = self.created_at.strftime("%Y-%m-%d %H:%M")
        return f"[{created}] {self.text}  (tags: {tags})"


class NotesBook(UserDict):
    def add(self, note: Note):
        # Використаємо простий індекс — зростаючий int як ключ (рядок)
        new_id = str(1 + max([int(k) for k in self.data.keys()], default=0))
        self.data[new_id] = note
        return new_id

    def edit(self, note_id: str, new_text: Optional[str] = None, new_tags: Optional[List[str]] = None):
        note = self.data.get(note_id)
        if not note:
            raise KeyError(f"No note with id {note_id}")
        if new_text is not None:
            note.text = new_text.strip()
        if new_tags is not None:
            note.tags = sorted({t.strip().lower() for t in new_tags if t.strip()})

    def delete(self, note_id: str):
        if note_id not in self.data:
            raise KeyError(f"No note with id {note_id}")
        self.data.pop(note_id)

    def search_text(self, query: str) -> Dict[str, Note]:
        q = query.lower().strip()
        return {nid: n for nid, n in self.data.items() if q in n.text.lower()}

    def search_tags(self, tags: List[str]) -> Dict[str, Note]:
        tagset = {t.strip().lower() for t in tags if t.strip()}
        return {nid: n for nid, n in self.data.items() if tagset.issubset(set(n.tags))}

    def sorted_by_tag(self) -> List[tuple]:
        # Повертає [(id, Note)] відсортовані за першою міткою (або "")
        return sorted(self.data.items(), key=lambda kv: (kv[1].tags[0] if kv[1].tags else ""))

    def to_list(self) -> List[Dict]:
        return [{"id": nid, **note.to_dict()} for nid, note in self.data.items()]

    @staticmethod
    def from_list(items: List[Dict]) -> "NotesBook":
        nb = NotesBook()
        for d in items:
            nid = str(d.get("id"))
            nb.data[nid] = Note.from_dict(d)
        return nb


# =========================
# Збереження на диск
# =========================
def load_all() -> tuple[AddressBook, NotesBook]:
    APP_DIR.mkdir(parents=True, exist_ok=True)
    # Contacts
    if CONTACTS_PATH.exists():
        try:
            contacts_data = json.loads(CONTACTS_PATH.read_text(encoding="utf-8"))
            book = AddressBook.from_list(contacts_data)
        except Exception:
            book = AddressBook()
    else:
        book = AddressBook()
    # Notes
    if NOTES_PATH.exists():
        try:
            notes_data = json.loads(NOTES_PATH.read_text(encoding="utf-8"))
            notes = NotesBook.from_list(notes_data)
        except Exception:
            notes = NotesBook()
    else:
        notes = NotesBook()
    return book, notes


def save_all(book: AddressBook, notes: NotesBook) -> None:
    CONTACTS_PATH.write_text(json.dumps(book.to_list(), ensure_ascii=False, indent=2), encoding="utf-8")
    NOTES_PATH.write_text(json.dumps(notes.to_list(), ensure_ascii=False, indent=2), encoding="utf-8")


# =========================
# Команди контактів
# =========================
@input_error
def cmd_add(args, book: AddressBook):
    """
    add [name] [phone] - створити контакт або додати телефон
    """
    name, phone = args
    rec = book.find(name)
    msg = "Contact updated."
    if rec is None:
        rec = Record(name)
        book.add_record(rec)
        msg = "Contact added."
    rec.add_phone(phone)
    return msg


@input_error
def cmd_add_email(args, book: AddressBook):
    """
    add-email [name] [email]
    """
    name, email = args
    rec = book.find(name)
    if not rec:
        raise KeyError
    rec.set_email(email)
    return "Email set."


@input_error
def cmd_add_address(args, book: AddressBook):
    """
    add-address [name] [address...]
    """
    name, *addr = args
    if not addr:
        raise ValueError("Provide address text.")
    rec = book.find(name)
    if not rec:
        raise KeyError
    rec.set_address(" ".join(addr))
    return "Address set."


@input_error
def cmd_change(args, book: AddressBook):
    """
    change [name] [old_phone] [new_phone]
    """
    name, old_phone, new_phone = args
    rec = book.find(name)
    if rec:
        rec.edit_phone(old_phone, new_phone)
        return "Contact changed."
    else:
        raise KeyError


@input_error
def cmd_del_phone(args, book: AddressBook):
    """
    del-phone [name] [phone]
    """
    name, phone = args
    rec = book.find(name)
    if not rec:
        raise KeyError
    rec.remove_phone(phone)
    return "Phone removed."


@input_error
def cmd_del_contact(args, book: AddressBook):
    """
    del-contact [name]
    """
    name = args[0]
    if not book.find(name):
        raise KeyError
    book.delete(name)
    return "Contact deleted."


@input_error
def cmd_phone(args, book: AddressBook):
    """
    phone [name]
    """
    name = args[0]
    rec = book.find(name)
    if rec:
        return "; ".join(p.value for p in rec.phones) or "-"
    else:
        raise KeyError


def cmd_all(book: AddressBook):
    """
    all
    """
    if not book.data:
        return "List is empty."
    return "\n".join(str(r) for r in book.data.values())


@input_error
def cmd_add_birthday(args, book: AddressBook):
    """
    add-birthday [name] [DD.MM.YYYY]
    """
    name, birthday_str = args
    rec = book.find(name)
    if not rec:
        raise KeyError
    rec.set_birthday(birthday_str)
    return "Birthday added."


@input_error
def cmd_show_birthday(args, book: AddressBook):
    """
    show-birthday [name]
    """
    name = args[0]
    rec = book.find(name)
    if rec:
        return rec.birthday.value.strftime(DATE_FMT) if rec.birthday else "Birthday not set for this contact."
    else:
        raise KeyError


def cmd_birthdays(args, book: AddressBook):
    """
    birthdays [days]  (за замовчуванням 7)
    """
    days = 7
    if args:
        try:
            days = int(args[0])
        except ValueError:
            return "Days must be integer."
    upcoming = book.birthdays_in(days)
    if not upcoming:
        return f"No upcoming birthdays in the next {days} day(s)."
    lines = [f"Upcoming birthdays in {days} day(s):"]
    for item in upcoming:
        lines.append(f"  {item['name']}: {item['congratulation_date']}")
    return "\n".join(lines)


def cmd_find(args, book: AddressBook):
    """
    find [query] — пошук по імені/телефону/email/адресі
    """
    if not args:
        return "Provide a search query."
    query = " ".join(args)
    results = book.search(query)
    if not results:
        return "No matches."
    return "\n".join(str(r) for r in results)


# =========================
# Команди нотаток
# =========================
@input_error
def cmd_note_add(args, notes: NotesBook):
    """
    note-add [text...] / опційно теги після --tags:  note-add Купити молоко --tags shopping,home
    """
    if not args:
        raise ValueError("Provide note text.")
    text, tags = _split_text_and_tags(args)
    nid = notes.add(Note(text, tags))
    return f"Note added with id {nid}."


@input_error
def cmd_note_edit(args, notes: NotesBook):
    """
    note-edit [id] [new text...] [--tags tag1,tag2]  (обидва поля опційні)
    """
    if not args:
        raise ValueError("Provide id.")
    nid = args[0]
    text, tags = _split_text_and_tags(args[1:])
    new_text = text if text else None
    new_tags = tags if tags is not None else None
    notes.edit(nid, new_text, new_tags)
    return "Note updated."


@input_error
def cmd_note_del(args, notes: NotesBook):
    """
    note-del [id]
    """
    nid = args[0]
    notes.delete(nid)
    return "Note deleted."


def cmd_note_list(notes: NotesBook):
    """
    note-list — вивід усіх нотаток
    """
    if not notes.data:
        return "No notes yet."
    return "\n".join([f"{nid}: {str(note)}" for nid, note in notes.data.items()])


def cmd_note_find(args, notes: NotesBook):
    """
    note-find [query] — пошук по тексту
    """
    if not args:
        return "Provide a search query."
    q = " ".join(args)
    found = notes.search_text(q)
    if not found:
        return "No matches."
    return "\n".join([f"{nid}: {str(note)}" for nid, note in found.items()])


def cmd_note_tags(args, notes: NotesBook):
    """
    note-tags [tag1,tag2] — пошук нотаток, що містять УСІ задані теги
    """
    if not args:
        return "Provide tags separated by comma."
    tags = [t.strip() for t in " ".join(args).split(",")]
    found = notes.search_tags(tags)
    if not found:
        return "No matches."
    return "\n".join([f"{nid}: {str(note)}" for nid, note in found.items()])


def cmd_note_sort(notes: NotesBook):
    """
    note-sort — відсортувати за першою міткою
    """
    if not notes.data:
        return "No notes yet."
    pairs = notes.sorted_by_tag()
    return "\n".join([f"{nid}: {str(note)}" for nid, note in pairs])


# =========================
# Допоміжне для тегів
# =========================
def _split_text_and_tags(args: List[str]) -> tuple[str, Optional[List[str]]]:
    """
    Розділяє список аргументів на:
    - текст нотатки (все до '--tags')
    - список тегів (після '--tags', через кому)
    """
    if "--tags" in args:
        idx = args.index("--tags")
        text = " ".join(args[:idx]).strip()
        tags_part = " ".join(args[idx + 1:]).strip()
        tags = [t.strip() for t in tags_part.split(",")] if tags_part else []
        return text, tags
    else:
        return " ".join(args).strip(), None


# =========================
# Парсер команд
# =========================
def parse_input(user_input: str):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def print_help():
    print("Available commands:")
    print("  hello / hi                 - Greeting")
    print("  add [name] [phone]         - Add a new contact or phone")
    print("  change [name] [old] [new]  - Change a phone number")
    print("  del-phone [name] [phone]   - Delete phone from contact")
    print("  del-contact [name]         - Delete contact")
    print("  add-email [name] [email]   - Set email (with validation)")
    print("  add-address [name] [addr]  - Set address")
    print("  phone [name]               - Show phones for a contact")
    print("  all                        - Show all contacts")
    print(f"  add-birthday [name] [{DATE_FMT}] - Add birthday")
    print("  show-birthday [name]       - Show a contact's birthday")
    print("  birthdays [days]           - Show upcoming birthdays")
    print("  find [query]               - Search in contacts")
    print("  note-add [text] [--tags t1,t2]         - Add note")
    print("  note-edit [id] [text] [--tags t1,t2]   - Edit note")
    print("  note-del [id]                          - Delete note")
    print("  note-list                               - List notes")
    print("  note-find [query]                       - Search notes by text")
    print("  note-tags [t1,t2]                       - Search notes by tags")
    print("  note-sort                               - Sort notes by tag")
    print("  save                                     - Save data to disk")
    print("  close / exit                            - Exit the bot")


# =========================
# Головний цикл
# =========================
def main():
    book, notes = load_all()
    print("444444 Welcome to the assistant bot! 444444")
    print("Type 'hello' for a greeting or 'help' for commands.")

    while True:
        try:
            user_input = input("Enter a command: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGood bye!")
            save_all(book, notes)
            break

        if not user_input:
            continue

        try:
            command, *args = parse_input(user_input)
        except ValueError:
            print("Invalid input.")
            continue

        if command in ["close", "exit"]:
            print("Good bye!")
            save_all(book, notes)
            break

        elif command in ["hello", "hi"]:
            print("How can I help you?")

        elif command == "help":
            print_help()

        # --- Contacts
        elif command == "add":
            print(cmd_add(args, book))
        elif command == "change":
            print(cmd_change(args, book))
        elif command == "del-phone":
            print(cmd_del_phone(args, book))
        elif command == "del-contact":
            print(cmd_del_contact(args, book))
        elif command == "add-email":
            print(cmd_add_email(args, book))
        elif command == "add-address":
            print(cmd_add_address(args, book))
        elif command == "phone":
            print(cmd_phone(args, book))
        elif command == "all":
            print(cmd_all(book))
        elif command == "add-birthday":
            print(cmd_add_birthday(args, book))
        elif command == "show-birthday":
            print(cmd_show_birthday(args, book))
        elif command == "birthdays":
            print(cmd_birthdays(args, book))
        elif command == "find":
            print(cmd_find(args, book))

        # --- Notes
        elif command == "note-add":
            print(cmd_note_add(args, notes))
        elif command == "note-edit":
            print(cmd_note_edit(args, notes))
        elif command == "note-del":
            print(cmd_note_del(args, notes))
        elif command == "note-list":
            print(cmd_note_list(notes))
        elif command == "note-find":
            print(cmd_note_find(args, notes))
        elif command == "note-tags":
            print(cmd_note_tags(args, notes))
        elif command == "note-sort":
            print(cmd_note_sort(notes))

        # --- Save
        elif command == "save":
            save_all(book, notes)
            print(f"Saved to: {CONTACTS_PATH} and {NOTES_PATH}")

        else:
            print("Invalid command. Type 'help' for a list of commands.")


if __name__ == "__main__":
    main()
