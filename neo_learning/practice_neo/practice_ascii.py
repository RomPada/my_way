
str = "Hello world!"

def conversation (str):
    dictionary = {}
    for sumbol in str:
       number = ord(sumbol) # ord() - функція приймає один символ і повертає його код ASCII
       dictionary [sumbol] = number
    return dictionary

print(conversation(str)) # друк одним рядком
