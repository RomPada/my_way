from pathlib import Path
import shutil

def sort_files_by_extension(dir_path):
    root = Path(dir_path)

    for item in root.rglob("*"):
        if item.is_file():
            ext = item.suffix.lstrip(".")
            folder = root / ext
            folder.mkdir(exist_ok=True)
            destination = folder / item.name
           
            if item.resolve() == destination.resolve():
                continue

            shutil.copy(item, destination)
            print("Створено папку:", folder)

sort_files_by_extension("D://Відрядження ОКП")
