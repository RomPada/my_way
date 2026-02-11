import heapq

# Function to calculate minimum cost to connect cables
def min_cost_to_connect_cables(cable_lengths: list[int]) -> int:
    heapq.heapify(cable_lengths)
    total_cost = 0
    while len(cable_lengths) > 1:
        cable1 = heapq.heappop(cable_lengths)
        cable2 = heapq.heappop(cable_lengths)
        current_cost = cable1 + cable2
        total_cost += current_cost
        heapq.heappush(cable_lengths, current_cost)
    return total_cost


cables = [4, 3, 2, 6]

print(f"Cabels: {cables}")
print(f"Min cost: {min_cost_to_connect_cables(list(cables))}")

