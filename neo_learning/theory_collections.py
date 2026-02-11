
import collections

# Створення іменованого кортежу Person
Person = collections.namedtuple('Person', ['first_name', 'last_name', 'age', 'birth_place', 'post_index'])

# Створення екземпляра Person
person = Person('Mick', 'Nitch', 35, 'Boston', '01146')

# Виведення різних атрибутів іменованого кортежу
print(person.first_name)       
print(person.post_index) 
print(person.age)        
print(person[3])         

# Ти можеш створювати стільки людей, скільки хочеш, використовуючи той самий шаблон Person:
person1 = Person('Mick', 'Nitch', 35, 'Boston', '01146')
person2 = Person('Alice', 'Brown', 28, 'New York', '10001')
person3 = Person('John', 'Smith', 42, 'Chicago', '60611')


#####
# Counter відноситься до модуля collections і служить для підрахунку хешабельних об'єктів. Це особливо корисно, коли 
# потрібно швидко підрахувати кількість окремих елементів у колекції, наприклад у списку, рядку або будь-якому іншому 
# ітерованому об'єкті. Counter функціонує як словник, де ключами є елементи, а значеннями - їх кількість у колекції.

import collections

student_marks = [4, 2, 4, 6, 7, 4, 2, 3, 4, 5, 6, 6, 7 , 1, 1, 1, 3, 5]
mark_counts = collections.Counter(student_marks)
print(mark_counts) # Counter({4: 4, 6: 3, 1: 3, 2: 2, 7: 2, 3: 2, 5: 2})


student_marks = [4, 2, 4, 6, 7, 4, 2 , 3, 4, 5, 6, 6, 7 , 1, 1, 1, 3, 5]
mark_counts = collections.Counter(student_marks)

print(mark_counts.most_common()) # [(4, 4), (6, 3), (1, 3), (2, 2), (7, 2), (3, 2), (5, 2)]
print(mark_counts.most_common(1)) # [(4, 4)]
print(mark_counts.most_common(2)) # [(4, 4), (6, 3)]

# Створення Counter з рядка
from collections import Counter
letter_count = Counter("banana")
print(letter_count) # Counter({'a': 3, 'n': 2, 'b': 1})

#####
sentence = "the quick brown fox jumps over the lazy dog"
words = sentence.split()
word_count = Counter(words)

# Виведення слова та його частоти
for word, count in word_count.items():
    print(f"{word}: {count}") # the: 2 quick: 1 brown: 1 fox: 1 jumps: 1 over: 1 lazy: 1 dog: 1


#####
# defaultdict

from collections import defaultdict

# Створення defaultdict з list як фабрикою за замовчуванням
d = defaultdict(list)

# Додавання елементів до списку для кожного ключа
d['a'].append(1)
d['a'].append(2)
d['b'].append(4)
print(d)

###
from collections import defaultdict

words = ['apple', 'zoo', 'lion', 'lama', 'bear', 'bet', 'wolf', 'appendix']
grouped_words = defaultdict(list)

for word in words:
    char = word[0]
    grouped_words[char].append(word)

print(dict(grouped_words))