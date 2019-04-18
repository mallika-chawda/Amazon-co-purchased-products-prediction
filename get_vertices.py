import numpy as np
import pandas as pd
import csv

edges = pd.read_csv("undirected_graph.csv")

source_nodes = set(edges['Source'])

target_nodes = set(edges['Target'])

all_nodes= source_nodes.union(target_nodes)

FileWriter = csv.writer(open("All_nodes.csv", 'w',  newline=''))

for node in all_nodes:
    FileWriter.writerow([str(node)])
    
