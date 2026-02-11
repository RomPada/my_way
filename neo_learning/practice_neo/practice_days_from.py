
# Наприклад ми хочемо визначити скільки пройшло повних днів, коли Наполеон спалив Москву, 
# а це відбулося 14 вересня 1812 року

from datetime import datetime
# Встановлення дати спалення Москви Наполеоном (14 вересня 1812 року)
napoleon_burns_moscow = datetime(year=1812, month=9, day=14)

# Поточна дата
current_date = datetime.now()

# Розрахунок кількості днів
days_since = current_date.toordinal() - napoleon_burns_moscow.toordinal()

print(days_since)


# а тепер переводимо кількість днів у роки, місяці та дні математично
years = days_since // 365
months = (days_since % 365) // 30
days_left = (days_since % 365) % 30

print(f"{years} років, {months} місяців і {days_left} днів")



### Конвертація datetime в timestamp та назад - !!!для загального розвитку!!!
### now = datetime.now() 
### timestamp = datetime.timestamp(now)
#
### timestamp = 1617183600
### dt_object = datetime.fromtimestamp(timestamp)
