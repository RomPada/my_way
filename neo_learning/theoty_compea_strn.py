
string1 = "Hello World"
string2 = "hello world"
if string1.lower() == string2.lower():
    print("Рядки однакові")
else:
    print("Рядки різні")

# casefold, який повертає рядок, де всі символи у нижньому регістрі 
# і без неоднозначностей, коли будь-який символ матиме тільки одну можливу форму запису.
text = "Python Programming"
print(text.casefold())
