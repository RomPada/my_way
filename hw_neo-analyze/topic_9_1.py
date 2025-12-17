import timeit

# Defin greedy algorithm to find coins
def find_coins_greedy(amount):
    coins = [50, 25, 10, 5, 2, 1]
    result = {}

    for coin in coins:
        if amount >= coin:
            count = amount // coin
            result[coin] = count
            amount -= coin * coun

    return result


# Define dynamic programming algorithm to find minimum coins
def find_min_coins(amount):
    coins = [50, 25, 10, 5, 2, 1]

    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    last_coin = [0] * (amount + 1)

    for i in range(1, amount + 1):
        for coin in coins:
            if i >= coin and dp[i - coin] + 1 < dp[i]:
                dp[i] = dp[i - coin] + 1
                last_coin[i] = coin

    result = {}
    current = amount

    while current > 0:
        coin = last_coin[current]
        result[coin] = result.get(coin, 0) + 1
        current -= coin

    return result


while True:
    try:
        amount = int(input("Input amount: "))
        if amount <= 0:
            print("Amount must be a positive integer.")
            continue
        break
    except ValueError:
        print("Please enter a number.")

coins = [50, 25, 10, 5, 2, 1]


print("Greedy approach:", find_coins_greedy(value))
print("Greedy approach time:", timeit.timeit(lambda: find_coins_greedy(value), number=1000))
print("Dynamic programming approach:", find_min_coins(value))
print("Dynamic programming approach time:", timeit.timeit(lambda: find_min_coins(value), number=1000))

