
import re
from typing import Callable, Iterator


def generator_numbers(text: str):

    padded = f" {text} "
    pattern = re.compile(r'(?<=\s)\d*\.?\d+(?=\s)')

    for m in pattern.finditer(padded):
        yield float(m.group())


def sum_profit(text: str, func):
    return sum(func(text))


if __name__ == "__main__":
    s = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів"
    print(f"Загальний дохід: {sum_profit (s, generator_numbers)} $")
