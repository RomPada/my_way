import random

# Definition of a binary tree node
class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

    def __str__(self, level=0, prefix="Root: "):
        ret = "\t" * level + prefix + str(self.val) + "\n"
        if self.left:
            ret += self.left.__str__(level + 1, "L--- ")
        if self.right:
            ret += self.right.__str__(level + 1, "R--- ")
        return ret

def insert(root, key):
    if root is None:
        return Node(key)
    else:
        if key < root.val:
            root.left = insert(root.left, key)
        else:
            root.right = insert(root.right, key)
    return root


# Create a sample binary search tree
root = Node(random.randint(30, 70))
for _ in range(10):
    root = insert(root, random.randint(1, 100))


# Function to find the sum of all nodes in the BST
def sum_value_node(root: Node | None) -> int:
    if root is None:
        raise ValueError("Tree is empty")
    sum = (root.val + sum_value_node(root.left) + sum_value_node(root.right))
    return sum
    
    
print(root)
print("Sum of all nodes is:", sum_value_node(root))

