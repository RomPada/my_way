
def dot_product(v1, v2):
    return sum(x*y for x, y in zip(v1, v2))

def get_orthogonal_pairs(vectors):
    n = len(vectors)
    orthogonal_pairs = []

    for i in range(n):
        for j in range(i+1, n):
            if dot_product(vectors[i], vectors[j]) == 0:
                orthogonal_pairs.append((i, j))

    return orthogonal_pairs

vectors = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 1]]
print(get_orthogonal_pairs(vectors))
