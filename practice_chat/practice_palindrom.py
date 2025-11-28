
def palindrom(word):
    if word == word[::-1]:
        return True
    else:
        return False

print(palindrom('level'))
print(palindrom('palindrome'))
