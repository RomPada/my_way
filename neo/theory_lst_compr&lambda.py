
# List comprehensions
nums = [1, 2, 3, 4, 5]
num = [2]
squared_nums = [x * y for x in nums for y in num]
print(squared_nums)

nums = [1, 2, 3, 4, 5]
num = [2]
squared_nums = [x * num[0] for x in nums]
print(squared_nums)


#####
# lambda arguments: expression

add = lambda x, y: x + y
print(add(5, 3))  # Виведе 8

nums1 = [1, 2, 3]
nums2 = [4, 5, 6]
sum_nums = map(lambda x, y: x + y, nums1, nums2)
print(list(sum_nums))


# lambda + filter
even_nums = filter(lambda x: x % 2 == 0, range(1, 11))
print(list(even_nums))
# or
print(list(filter(lambda x: x % 2 == 0, range(1, 11))))
