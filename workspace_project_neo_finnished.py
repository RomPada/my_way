# всі структури даних (Field, Record і так далі)

from datetime import datetime, date, timedelta

DATE_FORMAT = "%d.%m.%Y"

class AddressBook():
    def __init__(self):
        self.data = {}



    def get_upcoming_birthdays(self):  
        """
        Returns a list of contacts with upcoming birthdays within the specified period,
        taking into account the transfer of weekends to Monday.
        """
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
                'name': record.name.value,
                'birthday': record.birthday.value.strftime(DATE_FORMAT),
                'congratulation_date': congratulation_date.strftime(DATE_FORMAT)
            })

        return upcoming_birthdays

# Виведення, наприклад: 'name', birthday 'birthday' – need to wish 'congratulation_date' 
# Alex, birthday 15.11.1990 – need to wish 17.11.1990










































####  COMMANDS

# логіка виконання команд (add, phone, all і так далі)

from bot.utils import parse_input

def handle_command(user_input: str, book, notes):
    command, *args = parse_input(user_input)

    commands = {
        "hello": lambda: "How can I help you?",
    }

    if command in ("close", "exit"):
        return "exit"
    
    func = commands.get(command)
    if func:
        return func()
    else:
        print(f"Invalid command: {command}")

def birthdays(args, book):
    upcoming = book.get_upcoming_birthdays()
    if upcoming:
        result = []
        for birthday_info in upcoming:
            result.append(f"Congratulate {birthday_info['name']} on {birthday_info['congratulation_date']}")
        return "\n".join(result)
    else:
        return "No upcoming birthdays in the next week."