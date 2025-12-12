#  Програма візуалізує фрактал «сніжинка Коха». Користувач має можливість вказати рівень рекурсії.

import turtle
import math
import sys
from pathlib import Path


def koch_snowflake(t, order, size):
    if order == 0:
        t.forward(size)
    else:
        for angle in [60, -120, 60, 0]:
            koch_snowflake(t, order - 1, size / 3)
            t.left(angle)

def main():
    level = int(input("Введіть рівень рекурсії (наприклад, 3): "))
    size = 300  # Довжина сторони сніжинки

    window = turtle.Screen()
    window.title("Сніжинка Коха")
    t = turtle.Turtle()
    t.speed(0)  # Максимальна швидкість

    for _ in range(3):
        koch_snowflake(t, level, size)
        t.right(120)

    turtle.done()

if __name__ == "__main__":
    main()
