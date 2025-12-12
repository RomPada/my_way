import argparse
from pathlib import Path
import shutil
import sys


def copy_and_sort_files(src_dir: Path, dst_dir: Path) -> None:
    for item in src_dir.iterdir():
        try:
            if item.is_dir():
                if item.resolve() == dst_dir.resolve():
                    continue
                copy_and_sort_files(item, dst_dir)

            elif item.is_file():
                ext = item.suffix.lower().lstrip(".")
                if not ext:
                    ext = "no_extension"

                ext_folder = dst_dir / ext
                ext_folder.mkdir(parents=True, exist_ok=True)

                destination = ext_folder / item.name
                shutil.copy2(item, destination)

                print(f"Copy: {item} ---> {destination}")

        except Exception:
            print(f"Error")

def main(src, dst="dist"):
    src_dir = Path(src).resolve()
    dst_dir = Path(dst).resolve()
    
    if not src_dir.exists():
        print("Error: Source directory does not exist.")
        return

    dst_dir.mkdir(parents=True, exist_ok=True)
    copy_and_sort_files(src_dir, dst_dir)

    print("Done!")
