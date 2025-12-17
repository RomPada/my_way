import heapq
from collections import defaultdict

def dijkstra(graph, start):
    """
    graph: словник словників {вершина: {сусід: вага}}
    start: початкова вершина
    Повертає: distances (відстані), previous (для відновлення шляхів)
    """
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous = {node: None for node in graph}
    
    pq = [(0, start)]  # (відстань, вершина) — бінарна купа
    
    while pq:
        current_dist, current_node = heapq.heappop(pq)
        
        # Якщо цей запис застарілий — пропускаємо
        if current_dist > distances[current_node]:
            continue
        
        # Релаксація сусідів
        for neighbor, weight in graph[current_node].items():
            distance = current_dist + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))
    
    return distances, previous

# Функція для відновлення шляху до конкретної вершини
def get_path(previous, end):
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous[current]
    return path[::-1] if path and path[-1] == end else None



graph = {
    'A': {'B': 4, 'C': 2},
    'B': {'C': 1, 'D': 5},
    'C': {'B': 3, 'D': 8, 'E': 10},
    'D': {'E': 2},
    'E': {'D': 6}
}

distances, previous = dijkstra(graph, 'A')

print("Найкоротші відстані від A:")
for node, dist in distances.items():
    print(f"  До {node}: {dist if dist != float('inf') else '∞'}")

print("\nШляхи до вершин:")
for node in graph:
    if node != 'A':
        path = get_path(previous, node)
        if path:
            print(f"  До {node}: {' -> '.join(path)} (відстань {distances[node]})")