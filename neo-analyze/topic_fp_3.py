import heapq

# Клас для представлення графа
class Graph:
    def __init__(self):
        self.edges = {}
   
    # Додавання ребра
    def add_edge(self, u, v, weight, bidirectional=True):
        if u not in self.edges: self.edges[u] = {}
        if v not in self.edges: self.edges[v] = {}
        
        self.edges[u][v] = weight
        if bidirectional:
            self.edges[v][u] = weight

    # Отримання всіх вершин графа
    def get_nodes(self):
        return list(self.edges.keys())

# Алгоритм Дейкстри
def dijkstra(graph, start_node):
    shortest_paths = {node: float('inf') for node in graph.edges}
    shortest_paths[start_node] = 0
    predecessors = {node: None for node in graph.edges}
    priority_queue = [(0, start_node)]
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        if current_distance > shortest_paths[current_node]:
            continue
        for neighbor, weight in graph.edges[current_node].items():
            distance = current_distance + weight
            if distance < shortest_paths[neighbor]:
                shortest_paths[neighbor] = distance
                predecessors[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))
    return shortest_paths, predecessors

# Функція для відновлення шляху
def reconstruct_path(predecessors, target_node):
    path = []
    current = target_node
    while current is not None:
        path.append(current)
        current = predecessors[current]
    return " -> ".join(reversed(path))

# Головна частина програми
if __name__ == "__main__":
    g = Graph()
    # Додавання ребер до графа
    g.add_edge('A', 'B', 4)
    g.add_edge('A', 'C', 2)
    g.add_edge('B', 'C', 5)
    g.add_edge('B', 'D', 10)
    g.add_edge('C', 'E', 3)
    g.add_edge('E', 'D', 4)
    g.add_edge('D', 'F', 11)
    g.add_edge('E', 'F', 8)

    # Виведення доступних вершин
    available_nodes = g.get_nodes()
    print(f"Доступні вершини: {', '.join(sorted(available_nodes))}")
    
    # Введення початкової вершини користувачем
    while True:
        start_vertex = input("Введіть початкову точку (наприклад, A): ").strip().upper()
        if start_vertex in available_nodes:
            break
        print("Помилка: такої вершини немає в графі. Спробуйте ще раз.")

    distances, preds = dijkstra(g, start_vertex)

    print("\n" + "="*60)
    print(f"{'Вершина':<10} | {'Відстань':<15} | {'Маршрут'}")
    print("-" * 60)

    # Виведення результатів
    for node in sorted(distances.keys()):
        dist = distances[node]
        if dist == float('inf'):
            dist_str = "Недоступно"
            path_str = "-"
        else:
            dist_str = str(dist)
            path_str = reconstruct_path(preds, node)

        print(f"{node:<10} | {dist_str:<15} | {path_str}")
    print("="*60 + "\n")

