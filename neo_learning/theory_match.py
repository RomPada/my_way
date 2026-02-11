
# Оператор match - це свого роду розширена і більш гнучка версія оператора if-elif-else. 
# Він дозволяє порівнювати значення з рядом шаблонів і, залежно від відповідності, виконувати певні дії.
fruit = "apple"
match fruit:
    case "apple":
        print("This is an apple.")
    case "banana":
        print("This is a banana.")
    case "orange":
        print("This is an orange.")
    case _:
        print("Unknown fruit.")


point = (1, 0)
match point:
    case (0, 0):
        print("Точка в центрі координат")  
    case (0, y):
        print(f"Точка лежить на осі Y: y={y}")  
    case (x, 0):
        print(f"Точка лежить на осі X: x={x}") 
    case (x, y):
        print(f"Точка має координати:  x={x}, y={y}") 
    case _:
        print("Це не точка")
