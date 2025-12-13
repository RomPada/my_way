import networkx as nx
from collections import deque


G = nx.Graph()
G.add_edges_from([
    ("Kyiv", "Lviv"), 
    ("Kyiv", "Odessa"), 
    ("Kyiv", "Dnipro"), 
    ("Kyiv", "Kharkiv"), 
    ("Lviv", "Odessa"), 
    ("Dnipro", "Kharkiv")
])


# Алгоритм пошуку в глибину (DFS)
def dfs_path(graph, start, goal):
    stack = [(start, [start])]
    visited = set()
    while stack:
        node, path = stack.pop()
        if node == goal:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor in graph.neighbors(node):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))

# Алгоритм пошуку в ширину (BFS)
def bfs_path(graph, start, goal):
    queue = deque([(start, [start])])
    visited = set()
    while queue:
        node, path = queue.popleft()
        if node == goal:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor in graph.neighbors(node):
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))


print("BFS path from Lviv to Kharkiv:", bfs_path(G, "Lviv", "Kharkiv")) # ['Lviv', 'Kyiv', 'Kharkiv']
# Примітка: DFS-шлях може відрізнятися, бо залежить від порядку сусідів у графі.
print("DFS path from Lviv to Kharkiv:", dfs_path(G, "Lviv", "Kharkiv")) # ['Lviv', 'Odessa', 'Kyiv', 'Kharkiv']

