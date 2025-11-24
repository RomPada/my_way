
users = [
    {"name": "John Doe", "birthday": "1978.10.25"},
    {"name": "Jane Smith", "birthday": "2008.10.26"},
    {"name": "Adam Sendler", "birthday": "year.10.26"},
    {"name": "Johnny Depp", "birthday": "1963.06.09"}
    ]


def get_upcoming_birthdays(users):
    upcoming_birthdays = []
    from datetime import datetime, date, timedelta
    for user in users:
        try:
            birthday = datetime.strptime(user["birthday"], "%Y.%m.%d").date() # перетворюємо рядок днів народження у дати
            date_today = datetime.today().date() # визначення сьогодні
            birthday_this_year = birthday.replace(year=date_today.year)
            diff = birthday_this_year - date_today
            if diff >=  timedelta(days=7):
                pass
                #print("День народження пізніше.")
            elif diff < timedelta(days=0):
                pass
                #print("День народження минув.")
            else:
                if birthday_this_year.weekday() == 5:
                    #print("Це субота")
                    birthday_this_year = birthday_this_year + timedelta(days=2)
                    birthday_this_year = birthday_this_year.strftime("%Y.%m.%d")  
                    upcoming_birthdays.append({"name" : user["name"], "congratulation_date" : birthday_this_year})
                elif birthday_this_year.weekday() == 6:
                    #print("Це неділя")
                    birthday_this_year = birthday_this_year + timedelta(days=1)
                    birthday_this_year = birthday_this_year.strftime("%Y.%m.%d")  
                    upcoming_birthdays.append({"name" : user["name"], "congratulation_date" : birthday_this_year})
                else:
                    #print("Це робочий день")
                    birthday_this_year = birthday_this_year.strftime("%Y.%m.%d")  
                    upcoming_birthdays.append({"name" : user["name"], "congratulation_date" : birthday_this_year})
        except:
            print(f"{user["name"]} - дата народження у неправильному форматі. Ведіть дату у форматі РРРР.ММ.ДД.")
    print("Список привітань на цьому тижні:", upcoming_birthdays)
    return upcoming_birthdays 


get_upcoming_birthdays(users)
