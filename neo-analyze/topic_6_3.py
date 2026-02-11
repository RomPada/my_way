import networkx as nx


graph = {
    "Kyiv": {
        "Lviv": 540,
        "Odessa": 475,
        "Dnipro": 480,
        "Kharkiv": 480
    },
    "Lviv": {
        "Kyiv": 540,
        "Odessa": 790
    },
    "Odessa": {
        "Kyiv": 475,
        "Lviv": 790
    },
    "Dnipro": {
        "Kyiv": 480,
        "Kharkiv": 215
    },
    "Kharkiv": {
        "Kyiv": 480,
        "Dnipro": 215
    }
}


def build_path(parent, target):
    path = []
    while target is not None:
        path.append(target)
        target = parent[target]
    return list(reversed(path))

def dijkstra(graph, start):
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0
    parent = {vertex: None for vertex in graph}
    unvisited = list(graph.keys())
    while unvisited:
        current = min(unvisited, key=lambda v: distances[v])
        if distances[current] == float('infinity'):
            break
        for neighbor, weight in graph[current].items():
            new_distance = distances[current] + weight
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                parent[neighbor] = current
        unvisited.remove(current)
    return distances, parent


results = {}

for city in graph:
    dist, parents = dijkstra(graph, city)

    paths = {}
    for other_city in graph:
        paths[other_city] = build_path(parents, other_city)

    results[city] = {
        "distances": dist,
        "paths": paths
    }

for start in results:
    print(f"\nПочаткова вершина: {start}")
    print("Відстань   Шляхи:")
    for node in results[start]["paths"]:
        dist = results[start]["distances"][node]
        path = results[start]["paths"][node]
        print(f"{dist:<10} {start} -> {node}: {path}")

