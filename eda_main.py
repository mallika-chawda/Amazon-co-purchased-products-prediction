import re
import pandas as pd
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
import networkx as nx
import collections
from eda import get_edge_data, convert_to_unweighted, plot_degree_distribution

# Read Data into csv file
#get_edge_data('Amazon0302.txt', 'edge_data.csv')

# Convert Directed Graph to Undirected
# Get in-degree, out-degree and degree distributions
graph, degree, in_degree, out_degree = convert_to_unweighted('edge_data.csv')

# Store undirected graph in csv
nx.write_edgelist(graph, 'undirected_graph.csv', data = False, delimiter=',')

# Plot degree distributions
# Degree
plot_degree_distribution(degree, 'Degree Distribution', 'Degree', 'Count')

# In-degree
#plot_degree_distribution(in_degree, 'In-Degree Distribution', 'Degree', 'Count')

# Out-degree
#plot_degree_distribution(out_degree, 'Out-Degree Distribution', 'Degree', 'Count')

# Add Number_of_Copurchased Column to Meta Data to create Correlation Matrix

meta = pd.read_csv("amazon-meta.csv", encoding='iso-8859-1')
copurchased = []
meta['Average rating'] = meta['Average rating'].astype('float')

for idx, row in meta.iterrows():
    copurchased.append(degree[idx])
meta['Number_Co_Purchased'] = copurchased

# Item reviews vs Number of Co-Purchased Items
meta['Total reviews'] = meta['Total reviews'].astype('int64')

# meta.to_csv('meta_mod.csv')


# Title Similarity 
# Formula = |words_in_title(A) (intersect) words_in_title(B)|
#           _________________________________________________
#             |words_in_title(A) (union) words_in_title(B)|

similarity = defaultdict(float)

'''
for edge in graph.edges:
    #print(meta['Title'].iloc[edge[0]])
    if str(meta['Title'].iloc[edge[0]]) != 'nan':
        words_in_titleA = set(str(meta['Title'].iloc[edge[0]]).strip().split())
        words_in_titleB = set(str(meta['Title'].iloc[edge[1]]).strip().split())
        similarity[edge[0]] = len(words_in_titleA & words_in_titleB)/len(words_in_titleA | words_in_titleB) 

sim = [val for key, val in similarity.items()]
plt.plot(sim)
'''

# Popularity (in-degree, x-axis) vs Co-purchased Items (out-degree, y-axis)
copurch_popu = []
for val in meta['Id']:
    #copurch_popu[key].append(val)
    copurch_popu.append(degree[val])
fig, ax = plt.subplots()
#co_purch = [val[1] for key,val in copurch_popu.items()]
#popularity = [val[0] for key, val in copurch_popu.items()] 
meta= meta.fillna(0)
popularity = meta['Sales rank'].astype('float')
norm_popularity= (popularity - min(popularity))/float(max(popularity)- min(popularity))
print(norm_popularity[0:5])
print(len(copurch_popu), len(popularity))
plt.scatter(norm_popularity, copurch_popu, color='b')
plt.show()
plt.title("Out-Degree Histogram")
plt.ylabel("Number of Co-Purchased Items")
plt.xlabel("Popular Item from Least to Most")
#ax.set_xticks([d + 0.4 for d in deg_out])
#ax.set_xticklabels(deg_out)
