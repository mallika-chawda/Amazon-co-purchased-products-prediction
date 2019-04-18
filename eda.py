import re
import pandas as pd
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
import networkx as nx
import collections

# Read edge data from Amazon Data File
def get_edge_data(fname, csv_name):
    # fname: File from which data is to be read
    # csv_name: File in which data is to be saved 
    source_nodes = []
    target_nodes = []

    count = 0
    with open(fname) as f:
        data = f.readlines()
    for line in data:
        if bool(re.match('^[0-9]', line)):
            edge = line.strip().split('\t')
            source_nodes.append(edge[0])
            target_nodes.append(edge[1])
            #print(count)
            count += 1
            if count % 100000 == 0:
                print(line)
                print(count)
    print(count)
    dataframe = pd.DataFrame(data= {'source':source_nodes, 'target':target_nodes})
    dataframe.to_csv(csv_name, index = False)

def convert_to_unweighted(csv_name):
    graph_df = pd.read_csv(csv_name)
    graph = graph_df.values # Creating numpy array

    out_degree = defaultdict(int)
    in_degree = defaultdict(int)
    degree = defaultdict(int)

    for edge in graph:
        out_degree[edge[0]] += 1
        in_degree[edge[1]] += 1
        degree[edge[0]] += 1
        degree[edge[1]] += 1

    graph_undirected = nx.convert_matrix.from_pandas_edgelist(graph_df)
    return graph_undirected, degree, in_degree, out_degree

def plot_degree_distribution(degree_data, title, xlab, ylab):
    # Plot degree distribution
    # degree_data is a dictionary containing the nodes(keys) and their degrees(values)

    degree_sequence = sorted([value for key, value in degree_data.items()])
    degreeCount = collections.Counter(degree_sequence)
    deg_in, cnt = zip(*degreeCount.items())

    fig, ax = plt.subplots()
    plt.bar(deg_in, cnt, width=0.80, color='b')

    plt.title(title)
    plt.ylabel(ylab)
    plt.xlabel(xlab)
    plt.show()


# SalesRank Analysis
# Popularity (in-degree, x-axis) vs Co-purchased Items (out-degree, y-axis)
'''
copurch_popu = defaultdict(list)
for key, val in in_degree.items():
    copurch_popu[key].append(val)
    copurch_popu[key].append(out_degree[key])
fig, ax = plt.subplots()
co_purch = [val[1] for key,val in copurch_popu.items()]
popularity = [val[0] for key, val in copurch_popu.items()] 
print(len(co_purch), len(popularity))
plt.scatter(popularity, co_purch, color='b')

plt.title("Out-Degree Histogram")
plt.ylabel("Number of Co-Purchased Items")
plt.xlabel("Popular Item from Least to Most")
#ax.set_xticks([d + 0.4 for d in deg_out])
#ax.set_xticklabels(deg_out)
'''
'''
# Item Rating correlation with Number of Co-Purchased Items
meta = pd.read_csv("amazon-meta.csv", encoding='iso-8859-1')
copurchased = []
meta['Average rating'] = meta['Average rating'].apply(lambda x: float(x))
print(meta['Average rating'].unique())

for idx, row in meta.iterrows():
    if (type(meta['Similar'].iloc[idx])) != str:
        copurchased.append(0)
    else:
        similar_items = meta['Similar'].iloc[idx].strip().split()
        copurchased.append(len(similar_items))
meta['Number_Co_Purchased'] = copurchased

# Item reviews vs Number of Co-Purchased Items
meta['Total reviews'] = meta['Total reviews'].apply(lambda x: int(x))

correlations = meta.corr()
# plot correlation matrix
fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.matshow(correlations, vmin=-1, vmax=1)
fig.colorbar(cax)
ticks = np.arange(0,9,1)
ax.set_xticks(ticks)
ax.set_yticks(ticks)
ax.set_xticklabels(meta.columns, rotation = 45)
ax.set_yticklabels(meta.columns)
plt.show()
'''