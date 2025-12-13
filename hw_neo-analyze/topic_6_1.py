import networkx as nx
import matplotlib.pyplot as plt


G = nx.Graph()
G.add_edges_from([
    ("Kyiv", "Lviv"), 
    ("Kyiv", "Odessa"), 
    ("Kyiv", "Dnipro"), 
    ("Kyiv", "Kharkiv"), 
    ("Lviv", "Odessa"), 
    ("Dnipro", "Kharkiv")
])

nx.draw(G, node_size=2000, with_labels=True)
plt.show()

# Обчислення центральності вузлів
degree_centrality = nx.degree_centrality(G)     
# Обчислення центральності близькості вузлів 
closeness_centrality = nx.closeness_centrality(G)
# Обчислення проміжної центральності вузлів 
betweenness_centrality = nx.betweenness_centrality(G) 


print("Degree Centrality:", degree_centrality)
print("Closeness Centrality:", closeness_centrality)
print("Betweenness Centrality:", betweenness_centrality)

