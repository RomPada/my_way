
from collections import deque 

def palindrom(str):
    dq = deque(str)
    while len(dq) > 1:
        if dq.popleft() != dq.pop():
            return False
    return True

print(palindrom('level'))
print(palindrom('palindrome'))
