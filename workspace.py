def format_with_apostrophe(number):
    return f"{number:,}".replace(",", "'")


def factorial_step_by_step():
    n = int(input("Введіть число для обчислення факторіалу: "))

    if n < 0:
        print("Факторіал не визначений для від’ємних чисел")
        return

    result = 1
    print(f"\nОбчислення факторіалу числа {n}:")

    for i in range(1, n + 1):
        previous = result
        result *= i
        print(
            f"{format_with_apostrophe(previous)} × "
            f"{format_with_apostrophe(i)} = "
            f"{format_with_apostrophe(result)}"
        )

    print(
        f"\nРезультат: факторіал числа {n} = "
        f"{format_with_apostrophe(result)}"
    )


# Виклик функції
factorial_step_by_step()
