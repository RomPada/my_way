
import sys
from pathlib import Path
from colorama import init, Fore, Style

init(autoreset=True)

DIR_COLOR = Fore.BLUE + Style.BRIGHT
FILE_COLOR = Fore.GREEN
RESET = Style.RESET_ALL

def print_tree(path: Path, level: int = 0):
    try:
        for item in sorted(path.iterdir()):
            indent = " " * 4 * level
            if item.is_dir():
                print(f"{indent}{DIR_COLOR}{item.name}/{RESET}")
                print_tree(item, level + 1)
            else:
                print(f"{indent}{FILE_COLOR}{item.name}{RESET}")
    except:
        print("Помилка.")

def main():
    root_path = Path(sys.argv[1])
    if not root_path.exists():
        print("Шлях не існує.")
        sys.exit(1)
    if not root_path.is_dir():
        print("Це не директорія.")
        sys.exit(1)
    print(f"{DIR_COLOR}{root_path.name}/{RESET}")
    print_tree(root_path, 1)

if __name__ == "__main__":
    main()
