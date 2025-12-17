import heapq
from math import inf

def dijkstra_heap(graph, start):
    """
    graph: dict[str, list[tuple[str, int|float]]]
        Приклад: {"A": [("B", 5), ("C", 2)], ...}
    start: вершина-джерело

    Повертає:
      dist  - найкоротші відстані до всіх вершин
      prev  - попередники для відновлення шляху
    """
    dist = {v: inf for v in graph}
    prev = {v: None for v in graph}
    dist[start] = 0

    # (поточна_відстань, вершина)
    heap = [(0, start)]

    while heap:
        cur_dist, u = heapq.heappop(heap)

        # Якщо це "старий" запис (ми вже знайшли кращий шлях) — пропускаємо
        if cur_dist != dist[u]:
            continue

        # "Релаксація" ребер: пробуємо покращити сусідів
        for v, w in graph[u]:
            if w < 0:
                raise ValueError("Дейкстра не працює з від'ємними вагами ребер")

            new_dist = cur_dist + w
            if new_dist < dist[v]:
                dist[v] = new_dist
                prev[v] = u
                heapq.heappush(heap, (new_dist, v))

    return dist, prev


def reconstruct_path(prev, start, target):
    """Відновлює шлях start -> target по словнику prev."""
    path = []
    cur = target
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()

    if path and path[0] == start:
        return path
    return []  # якщо шлях не існує


# --- Приклад графа (орієнтований). Для неорієнтованого додавайте ребра в обидва боки.
graph = {
    "A": [("B", 4), ("C", 2)],
    "B": [("C", 1), ("D", 5)],
    "C": [("B", 1), ("D", 8), ("E", 10)],
    "D": [("E", 2)],
    "E": []
}

dist, prev = dijkstra_heap(graph, "A")

print("Відстані:", dist)
print("Шлях A -> E:", reconstruct_path(prev, "A", "E"))
