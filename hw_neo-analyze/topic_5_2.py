
def binary_search(arr, x):
    """
    Отримує відсортований масив та значення, яке необхідно знайти.
    Повертає кортеж з трьох елементів:
        1. Кількість ітерацій, необхідних для пошуку.
        2. Індекс знайденого значення.
        3. Знайдене значення.
            прим. 3 - У разі відсутності - None та найближче більше значення.
    """
    low = 0
    high = len(arr) - 1
    mid = 0
    counter = 0
    while low <= high:
        counter += 1
        mid = (high + low) // 2
        if arr[mid] < x:
            low = mid + 1
        elif arr[mid] > x:
            high = mid - 1
        else:
            element = arr[mid]
            return counter, mid, element
    element = arr[mid]
    return counter, None, element

numbers = [
    -19.4, -18.9, -17.3, -16.8, -15.2, -14.7, -13.1, -12.6, -11.0, -10.5,
    -9.9, -8.4, -7.8, -6.3, -5.9, -4.2, -3.7, -2.1, -1.6, -0.5,
     0.0, 0.8, 1.4, 2.0, 2.7, 3.3, 4.0, 4.6, 5.2, 5.9,
     6.3, 7.0, 7.8, 8.1, 9.0, 9.6, 10.2, 10.9, 11.4, 12.0,
]


print(binary_search(numbers, -17.3))

print(binary_search(numbers, 2.34))
print(binary_search(numbers, 2.7))

