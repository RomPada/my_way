
import turtle

T_STEP = 30
KOCH_ROTATIONS = [60, -120, 60, 0]

depth = int(input("Enter recursion level: "))

screen = turtle.Screen()
t = turtle.Turtle()

def draw_koch(n):
    if n == 0:
        t.forward(T_STEP)
    else:
        for angle in KOCH_ROTATIONS:
            draw_koch(n - 1)
            t.left(angle)

for _ in range(3):
    draw_koch(depth)
    t.left(-120)

screen.mainloop()
