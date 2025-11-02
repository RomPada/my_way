some_str = 'Видавництво А-БА-БА-ГА-ЛА-МА-ГА'

new_str = ''.join([x for x in some_str if x.isnumeric()])
print(new_str)

