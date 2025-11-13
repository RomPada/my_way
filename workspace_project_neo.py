from datetime import datetime, date, timedelta


# -----------------------------
# Заглушки для тестування
# -----------------------------

DATE_FORMAT = "%Y.%m.%d" ##############################################################

class Birthday:
    def __init__(self, value: str):
        # зберігаємо як date, як у твоєму основному коді
        self.value = datetime.strptime(value, DATE_FORMAT).date()


class Name:
    def __init__(self, value):
        self.value = value


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.birthday = Birthday(birthday) if birthday else None


class AddressBook:
    def __init__(self):
        self.data = {}
    
    # пропоную додати до класу, який буде відповідати за додавання та  відображення 
    def get_upcoming_birthdays(self):
        days_limit = int(input("How many days ahead should you search?"))
        today = date.today()
        upcoming_birthdays = []

        for record in self.data.values():
            if not record.birthday:
                continue

            birthday_date = record.birthday.value
            birthday_this_year = birthday_date.replace(year=today.year)

            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            days_until_birthday = (birthday_this_year - today).days

            if not (0 <= days_until_birthday <= days_limit):
                continue

            congratulation_date = birthday_this_year

            if congratulation_date.weekday() == 5:
                congratulation_date += timedelta(days=2)
            elif congratulation_date.weekday() == 6:
                congratulation_date += timedelta(days=1)

            upcoming_birthdays.append({
                "name": record.name.value,
                "birthday": record.birthday.value.strftime(DATE_FORMAT),
                "congratulation_date": congratulation_date.strftime(DATE_FORMAT)
            })

        return upcoming_birthdays


# -----------------------------
# Тестові дані
# -----------------------------

address_book = AddressBook()

address_book.data = {
    1: Record("Анна", "1995.11.15"),     # скоро (якщо зараз лютий)
    2: Record("Богдан", "1988.03.01"),   # ближче, ніж 10 днів
    3: Record("Катерина", "1990.12.30"), # далеко — не влізе у days_limit
    4: Record("Дмитро", "2000.02.15"),   # вчора/сьогодні/завтра — залежить від дати
    5: Record("Олена"),                  # без дня народження
}


# -----------------------------
# Запуск тесту
# -----------------------------


birthdays = address_book.get_upcoming_birthdays()

if birthdays:
    for b in birthdays:
        print("______________")
        print(f"{b['name']}, день народження {b['birthday']} – привітати {b['congratulation_date']}")
else:
    print("У вибраний період немає днів народження.")
