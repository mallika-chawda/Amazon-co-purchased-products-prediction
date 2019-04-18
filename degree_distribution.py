import collections
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np


# Network Metrics
edge_data = pd.read_csv('undirected_graph.csv').values
edges = [(e[0], e[1]) for e in edge_data]

G = nx.Graph(edges)

degree_sequence = sorted([d for n, d in G.degree()], reverse=True)  # degree sequence
# print "Degree sequence", degree_sequence
degreeCount = collections.Counter(degree_sequence)
deg, cnt = zip(*degreeCount.items())

total_cnt= sum(cnt)
cnt= [i/float(total_cnt) for i in list(cnt)]

fig, ax = plt.subplots()
plt.bar(deg, cnt, width=0.80, color='b')

plt.title("Degree Histogram")
plt.ylabel("Count")
plt.xlabel("Degree")
#ax.set_xticks([])
#ax.set_xticklabels(deg)

plt.show()