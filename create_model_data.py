import re
import pandas as pd
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
import networkx as nx
import collections
import random
from nltk.stem import PorterStemmer 
from nltk.tokenize import word_tokenize
from datetime import datetime
import nltk
from util import get_edge_data, convert_to_undirected, plot_degree_distribution

nltk.download('punkt')

# Read Data into csv file
get_edge_data('Amazon0302.txt', 'edge_data.csv')
print("\nConverted Input Edge file into CSV")

# Convert Directed Graph to Undirected
# Get in-degree, out-degree and degree distributions

graph, degree, in_degree, out_degree = convert_to_undirected('edge_data.csv')
print("\nGot Undirected Graph\n")

# Store undirected graph in csv
nx.write_edgelist(graph, 'undirected_graph.csv', data = False, delimiter=',')

# Read and Manipulate Meta Data
meta = pd.read_csv("amazon-meta.csv", encoding='iso-8859-1')
print("Read meta data\n")

# Title Similarity 
# Formula = |words_in_title(A) (intersect) words_in_title(B)|
#           _________________________________________________
#             |words_in_title(A) (union) words_in_title(B)|


# Pairs Group Attributes
unique_groups = meta['Group'].unique()
unique_groups = [i for i in unique_groups if str(i) != 'nan']

pairs_table = pd.DataFrame(0,index = unique_groups, columns =  unique_groups)
undirected_edges = pd.read_csv('undirected_graph.csv').values
for edge in undirected_edges:
    group1 = meta.iloc[edge[0]]['Group']
    group2 = meta.iloc[edge[1]]['Group']
    if str(group1) != 'nan' and str(group2) != 'nan':
        pairs_table.at[group1, group2] += 1
        if group1 != group2:
            pairs_table.at[group2, group1] +=1 

#print(pairs_table)
pairs_table.to_csv("pairs_table.csv")


#########################################################################
#########################################################################
########################### CREATE MODEL DATA ###########################

# Required Features:
# 1. Title Similarity
# 2. Sales Rank (Diff between that of the two nodes)
# 3. Average Rating (Diff)
# 4. Time of First Review of Two Items 
# 5. Group (Binary based on whether the two nodes have the same group)

# Create Initial model dataframe    

node1 = []
node2 = []
labels = []
count = 0
n = graph.number_of_edges() # n is the number of edges in the network
for edge in list(graph.edges):
    node1.append(edge[0])
    node2.append(edge[1])
    labels.append(1)
model_data = pd.DataFrame(data = {'node1':node1, 'node2':node2, 'label':labels})

node1 = []
node2 = []
labels = []
m = len(meta['Id']) # Number of nodes
for i in range(1, m):
    node_1, node_2 = random.sample(range(1,m), 2)
    edge = (node_1, node_2)

    while graph.has_edge(*edge):
        node_1, node_2 = random.sample(range(1,m), 2) 
        edge = (node_1, node_2)
    
    graph.add_edge(*edge)
    node1.append(int(node_1))
    node2.append(int(node_2))
    labels.append(0)
    #count += 1
    #if count % 100000 == 0:
    #    print(count)
model_data_0 = pd.DataFrame(data = {'node1':node1, 'node2':node2, 'label':labels})
model_data = pd.concat([model_data, model_data_0])
model_data.to_csv('model_data_init.csv', index = False)
print("\n\n Created Initial Data\n\n")

# Read final model data from initial model dataframe
model_data = pd.read_csv('model_data_init.csv')
model_data_vals = model_data.values

# Create the remaining feature columns
title_sim = []
sales_rank_diff = []
avg_rating_diff = []
time_diff = []
group_compare = []
category_sim = []
count = 0
ps = PorterStemmer()
for edge in model_data_vals:
    node1 = edge[0]
    node2 = edge[1]
    # Group
    group1 = meta.iloc[node1]['Group']
    group2 = meta.iloc[node2]['Group']
    if str(group1) != 'nan' and str(group2) != 'nan':
        if group1 == group2:
            group_compare.append(1)
        else:
            group_compare.append(0)
    else:
        group_compare.append(0)
    
    # Title Similarity
    if str(meta['Title'].iloc[node1]) != 'nan' and str(meta['Title'].iloc[node2]) != 'nan':
        words_in_titleA = word_tokenize(str(meta['Title'].iloc[node1])) 
        words_in_titleB = word_tokenize(str(meta['Title'].iloc[node2]))
        stem_A = set([ps.stem(w) for w in words_in_titleA])
        stem_B = set([ps.stem(w) for w in words_in_titleB])
        similarity = float(len(stem_A & stem_B))/float(len(stem_A | stem_B)) 
        title_sim.append(similarity)
    else:
        title_sim.append(0)

    # Sales Ranks
    if str(meta['Sales rank'].iloc[node1]) != 'nan' and str(meta['Sales rank'].iloc[node2]) != 'nan':
        sales_rank_diff.append(abs(int(meta['Sales rank'].iloc[node1]) - int(meta['Sales rank'].iloc[node2])))
    elif str(meta['Sales rank'].iloc[node1]) != 'nan' and str(meta['Sales rank'].iloc[node2]) == 'nan':
        sales_rank_diff.append(int(meta['Sales rank'].iloc[node1]))
    elif str(meta['Sales rank'].iloc[node1]) == 'nan' and str(meta['Sales rank'].iloc[node2]) != 'nan':
        sales_rank_diff.append(int(meta['Sales rank'].iloc[node2]))
    else:
        sales_rank_diff.append(0)

    # Average Rating
    if str(meta['Average rating'].iloc[node1]) != 'nan' and str(meta['Average rating'].iloc[node2]) != 'nan':
        avg_rating_diff.append(abs(float(meta['Average rating'].iloc[node1]) - float(meta['Average rating'].iloc[node2])))
    elif str(meta['Average rating'].iloc[node1]) != 'nan' and str(meta['Average rating'].iloc[node2]) == 'nan':
        avg_rating_diff.append(float(meta['Average rating'].iloc[node1]))
    elif str(meta['Average rating'].iloc[node1]) == 'nan' and str(meta['Average rating'].iloc[node2]) != 'nan':
        avg_rating_diff.append(float(meta['Average rating'].iloc[node2]))
    else:
        avg_rating_diff.append(0)
    
    # Time Diff
    d = 0
    if str(meta['Date'].iloc[node1]) != 'nan' and str(meta['Date'].iloc[node2]) != 'nan':
        d1 = datetime.strptime(meta['Date'].iloc[node1], "%Y-%m-%d")
        d2 = datetime.strptime(meta['Date'].iloc[node2], "%Y-%m-%d")
        if d1>d2:
            d = d1-d2
        else:
            d = d2-d1
        d = d.days
    time_diff.append(d)

    # Category Similarity
    if str(meta['All categories'].iloc[node1]) != 'nan' and str(meta['All categories'].iloc[node2]) != 'nan':
        categoriesA = meta['All categories'].iloc[node1].split('-')
        categoriesB = meta['All categories'].iloc[node2].split('-')
        A = set([int(c) for c in categoriesA])
        B = set([int(c) for c in categoriesB])
        similarity = float(len(A & B))/float(len(A | B)) 
        category_sim.append(similarity)
    else:
        category_sim.append(0)

    if count % 100000 == 0:
        print(count)
    count += 1

model_data['Group'] = group_compare
model_data['Title Similarity'] = title_sim
model_data['Time'] = time_diff
model_data['Average Rating'] = avg_rating_diff
model_data['Sales Rank'] = sales_rank_diff
model_data['Category Similarity'] = category_sim
model_data = model_data[['node1', 'node2' , 'Group', 'Category Similarity', 'Title Similarity', 'Time', 'Average Rating', 'Sales Rank', 'label']]

print("\n\n\nData Preview\n\n")
print(model_data.head(10))
model_data.to_csv('model_data_final.csv', index = False)
