from pathlib import Path

def print_tree(root: Path, prefix: str = "") -> None:
    """
    Виводить дерево файлів та папок, починаючи з директорії root.

    root   – Path до директорії, з якої починаємо
    prefix – службовий рядок для відступів (використовується рекурсією)
    """

    # Отримуємо список елементів у папці
    # Спочатку папки, потім файли, все – по імені
    items = sorted(
        root.iterdir(),
        key=lambda p: (not p.is_dir(), p.name.lower())
    )

    for index, item in enumerate(items):
        is_last = (index == len(items) - 1)
        connector = "└── " if is_last else "├── "

        print(prefix + connector + item.name)

        # Якщо це папка – заходимо в неї рекурсивно
        if item.is_dir():
            # Для останнього елемента – відступ без вертикальної лінії
            new_prefix = prefix + ("    " if is_last else "│   ")
            print_tree(item, new_prefix)


def main():
    start_dir = Path("D://Техавіаком-2")
    if not start_dir.exists():
        print("Помилка: вказана директорія не існує")
        return

    print(start_dir)  # виводимо корінь
    print_tree(start_dir)


if __name__ == "__main__":
    main()
