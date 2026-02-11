import uuid
from collections import deque

import networkx as nx
import matplotlib.pyplot as plt


class Node:
    def __init__(self, key, color="#222222"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())


# Рекурсивна функція для додавання ребер до графа
def add_edges(graph, node, pos, x=0, y=0, layer=1):
    if node is not None:
        graph.add_node(node.id, color=node.color, label=str(node.val))
        pos[node.id] = (x, y)

        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2 ** layer
            add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)

        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)

    return graph


# Функція для підрахунку кількості вузлів у дереві (BFS)
def count_nodes_bfs(root: Node) -> int:
    if root is None:
        return 0
    q = deque([root])
    cnt = 0
    while q:
        node = q.popleft()
        cnt += 1
        if node.left:
            q.append(node.left)
        if node.right:
            q.append(node.right)
    return cnt


# Функція для генерації градієнтних кольорів у HEX форматі
def gradient_hex_colors(n, dark=(15, 35, 70), light=(170, 220, 255)):
    if n <= 1:
        r, g, b = light
        return [f"#{r:02X}{g:02X}{b:02X}"]

    colors = []
    for i in range(n):
        t = i / (n - 1)  # 0..1
        r = int(dark[0] + (light[0] - dark[0]) * t)
        g = int(dark[1] + (light[1] - dark[1]) * t)
        b = int(dark[2] + (light[2] - dark[2]) * t)
        colors.append(f"#{r:02X}{g:02X}{b:02X}")
    return colors


# DFS (обхід у глибину) БЕЗ рекурсії
def dfs_iterative(root: Node):
    """
    DFS (обхід у глибину) БЕЗ рекурсії.
    Використовуємо стек.
    Порядок: root -> left -> right
    """
    order = []
    if root is None:
        return order

    stack = [root]
    while stack:
        node = stack.pop()
        order.append(node)

        # Щоб обійти left раніше, right кладемо в стек першим
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)

    return order


# BFS (обхід у ширину) БЕЗ рекурсії
def bfs_iterative(root: Node):
    """
    BFS (обхід у ширину) БЕЗ рекурсії.
    Використовуємо чергу.
    """
    order = []
    if root is None:
        return order

    q = deque([root])
    while q:
        node = q.popleft()
        order.append(node)

        if node.left:
            q.append(node.left)
        if node.right:
            q.append(node.right)

    return order


# Функція для візуалізації бінарного дерева
def draw_tree(root: Node, title: str):
    G = nx.DiGraph()
    pos = {}
    add_edges(G, root, pos)

    node_colors = [G.nodes[n].get("color", "#222222") for n in G.nodes()]
    labels = {n: G.nodes[n].get("label", "") for n in G.nodes()}

    plt.clf()
    plt.title(title)
    nx.draw(
        G,
        pos=pos,
        labels=labels,
        with_labels=True,
        node_color=node_colors,
        node_size=1800,
        arrows=False,
        font_size=12
    )
    plt.axis("off")


# Візуалізація обходу дерева
def visualize_traversal(root: Node, traversal_name: str, order_nodes, pause_sec=0.9):
    all_count = count_nodes_bfs(root)
    base_color = "#2A2A2A"

    all_nodes = bfs_iterative(root)
    for n in all_nodes:
        n.color = base_color

    colors = gradient_hex_colors(len(order_nodes))

    plt.figure(figsize=(10, 6))

    for step, (node, c) in enumerate(zip(order_nodes, colors), start=1):
        node.color = c
        draw_tree(root, f"{traversal_name} — крок {step}/{len(order_nodes)}")
        plt.pause(pause_sec)

    plt.show()


# ПРИКЛАД ДЕРЕВА 
def build_demo_tree():
    #      10
    #     /  \
    #    5    15
    #   / \     \
    #  2   7     20
    root = Node(10)
    root.left = Node(5)
    root.right = Node(15)
    root.left.left = Node(2)
    root.left.right = Node(7)
    root.right.right = Node(20)
    return root


if __name__ == "__main__":
    root = build_demo_tree()

    # DFS (стек)
    dfs_order = dfs_iterative(root)
    visualize_traversal(root, "DFS (обхід у глибину, стек)", dfs_order, pause_sec=0.8)

    # BFS (черга)
    bfs_order = bfs_iterative(root)
    visualize_traversal(root, "BFS (обхід у ширину, черга)", bfs_order, pause_sec=0.8)

