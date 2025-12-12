
import timeit
import random


### Реалізація алгоритму сортування злиттям (Merge Sort) на Python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]

    return merge(merge_sort(left_half), merge_sort(right_half))

def merge(left, right):
    merged = []
    left_index = 0
    right_index = 0

    while left_index < len(left) and right_index < len(right):
        if left[left_index] <= right[right_index]:
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1

    while left_index < len(left):
        merged.append(left[left_index])
        left_index += 1

    while right_index < len(right):
        merged.append(right[right_index])
        right_index += 1

    return merged


### Реалізація алгоритму сортування вставками (Insertion Sort) на Python
def insertion_sort(lst):
    for i in range(1, len(lst)):
        key = lst[i]
        j = i-1
        while j >=0 and key < lst[j] :
                lst[j+1] = lst[j]
                j -= 1
        lst[j+1] = key 
    return lst


# Генерація випадкового списку чисел
def make_list(a, b):
    return [random.randint(1, 1000) for _ in range(random.randint(a, b))]

numbers, numbers_2, numbers_3 = (make_list(a, b) for a, b in [(10, 50), (100, 200), (400, 600)])


print(
    f"List length within 10-50: {len(numbers)}\n"
    f"Time insertion sort: {timeit.timeit(lambda: insertion_sort(numbers), number=1000)}\n"
    f"Time merge sort: {timeit.timeit(lambda: merge_sort(numbers), number=1000)}\n"
    f"Time sorted (Timsort): {timeit.timeit(lambda: sorted(numbers), number=1000)}\n"
    "-------"
)

print(
    f"List length within 100-200: {len(numbers_2)}\n"
    f"Time insertion sort: {timeit.timeit(lambda: insertion_sort(numbers), number=1000)}\n"
    f"Time merge sort: {timeit.timeit(lambda: merge_sort(numbers), number=1000)}\n"
    f"Time sorted (Timsort): {timeit.timeit(lambda: sorted(numbers), number=1000)}\n"
    "-------"
)

print(
    f"List length within 400-600: {len(numbers_3)}\n"
    f"Time insertion sort: {timeit.timeit(lambda: insertion_sort(numbers_3), number=1000)}\n"
    f"Time merge sort: {timeit.timeit(lambda: merge_sort(numbers_3), number=1000)}\n"
    f"Time sorted (Timsort): {timeit.timeit(lambda: sorted(numbers_3), number=1000)}\n"
    "-------"
)

