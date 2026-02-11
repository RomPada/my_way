
# Напиши програму, яка виводить числа від 1 до N (включно), але:
# якщо число кратне 3, замість числа виведи слово "Fizz",
# якщо число кратне 5, замість числа виведи слово "Buzz",
# якщо число кратне одночасно 3 і 5, виведи "FizzBuzz".
# Усі інші числа потрібно виводити як є.

n = int(input("Введіть число: "))
nums = list(range(1, n + 1))

for num in nums:
    if num % 3 == 0 and num % 5 == 0:
        print ("FizzBuzz")
    elif num % 3 == 0:
        print ("Fizz")
    elif num % 5 == 0:
        print ("Buzz")
    else:
        print (num)

#print (nums)
