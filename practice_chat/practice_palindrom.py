
def palindrom(word):
    if word == word[::-1]:
        print('+')
    else:
        print('-')

palindrom('ama')
palindrom('amnyya')
