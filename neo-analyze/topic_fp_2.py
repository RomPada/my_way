import turtle

def draw_pythagoras_tree(t, branch_len, level):
    """
    Рекурсивна функція для малювання дерева.
    
    t: об'єкт turtle (черепашка)
    branch_len: довжина поточної гілки
    level: рівень рекурсії (глибина)
    """
    if level == 0:
        return
    t.forward(branch_len)
    angle = 45
    t.right(angle)
    draw_pythagoras_tree(t, branch_len * 0.7, level - 1)
    t.left(angle * 2)
    draw_pythagoras_tree(t, branch_len * 0.7, level - 1)
    t.right(angle)
    t.backward(branch_len)

def main():
    screen = turtle.Screen()
    screen.title("Фрактал 'Дерево Піфагора'")
    screen.bgcolor("white")
    t = turtle.Turtle()
    t.color("brown")
    t.speed("fastest")
    t.hideturtle()
    t.left(90)
    t.penup()
    t.goto(0, -250)
    t.pendown()
    try:
        level = int(screen.textinput("Введення даних", "Введіть рівень рекурсії (наприклад, 8-12):"))
    except (ValueError, TypeError):
        level = 8
    initial_length = 100 
    draw_pythagoras_tree(t, initial_length, level)
    screen.mainloop()

if __name__ == "__main__":
    main()

