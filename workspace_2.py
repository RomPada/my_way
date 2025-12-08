import argparse
from pathlib import Path
import shutil
import sys


def copy_and_sort_files(src_dir: Path, dst_dir: Path) -> None:
    """
    Рекурсивно проходить по всіх файлах у src_dir
    та копіює їх у dst_dir, розкладаючи по підпапках за розширенням.
    """
    for item in src_dir.iterdir():
        try:
            # Якщо це папка — заходимо в неї рекурсивно
            if item.is_dir():
                # Захист від зациклення, якщо dst_dir всередині src_dir
                if item.resolve() == dst_dir.resolve():
                    continue
                copy_and_sort_files(item, dst_dir)

            # Якщо це файл — копіюємо
            elif item.is_file():
                # Беремо розширення без крапки, у нижньому регістрі
                ext = item.suffix.lower().lstrip(".")

                # Якщо розширення немає — кладемо в спеціальну папку
                if not ext:
                    ext = "no_extension"

                # Папка призначення для цього типу файлів
                ext_folder = dst_dir / ext
                ext_folder.mkdir(parents=True, exist_ok=True)

                destination = ext_folder / item.name

                # Копіюємо файл з метаданими (час зміни, права і т.д.)
                shutil.copy2(item, destination)

                print(f"Скопійовано: {item} -> {destination}")

        except PermissionError as e:
            print(f"Немає доступу до: {item}. Помилка: {e}")
        except OSError as e:
            print(f"Помилка при обробці: {item}. Помилка: {e}")


def main(src, dst="dist"):
    src_dir = Path(src).resolve()
    dst_dir = Path(dst).resolve()
    
    if not src_dir.exists():
        print("Помилка: вихідна директорія не існує")
        return

    dst_dir.mkdir(parents=True, exist_ok=True)
    copy_and_sort_files(src_dir, dst_dir)

    print("Готово!")



main("D://Відрядження ОКП", "D://Відрядження ОКП//sorted_files")