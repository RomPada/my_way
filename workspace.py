arr = [1, 3, 5, 7, 9, 11, 14, 16, 18, 20, 22, 25, 28, 30]
key = 25
low = 0 
high = len(arr) - 1 # 13
index = int(low + ((key - arr[low]) / (arr[high] - arr[low])) * (high - low)) # 10
print(index)