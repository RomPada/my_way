
from collections import deque 

def palindrom(str: str) -> bool:
    # видаляємо пробіли на початку і в кінці рядка ↓
    # str = str.strip()
    # видаляємо всі пробіли в рядку і робимо всі букви маленькими ↓
    str = str.replace(" ", "").lower()
    dq = deque(str)
    while len(dq) > 1:
        if dq.popleft() != dq.pop():
            return False
    return True

print(palindrom('level'))
print(palindrom('palindrome'))
