import pandas as pd
import numpy as np
import networkx as nx
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_validate
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, normalize

'''
# Network Metrics
edge_data = pd.read_csv('undirected_graph.csv').values
edges = [(e[0], e[1]) for e in edge_data]

G = nx.Graph(edges)
avg_path_length = nx.average_shortest_path_length(G)
print("Avg Path Length = ", avg_path_length)
'''

# Read model data
data = pd.read_csv('model_data_final2.csv')[1:1448344]
features = ['Group', 'Category Similarity', 'Title Similarity', 'Time', 'Average Rating', 'Sales Rank']
#features = ['Sales Rank', 'Category Similarity']

#filtering out data
data= data[(data['Category Similarity']>0) | (data['Title Similarity']>0) | (data['Time']>0)]

X = data[features]
y = data['label']

# Model 1 - Logistic Regression
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size = 0.8)
logreg = LogisticRegression().fit(X_train, y_train)
pred_prob = logreg.predict_proba(X_test)
pred = [1 if i[1] >= 0.50 else 0 for i in pred_prob]
acc = accuracy_score(y_test, pred)
print(acc)

scaler = StandardScaler().fit(data)
data = scaler.transform(data)
#data = normalize(data)
#print(data[1:10])
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size = 0.8)
logreg = LogisticRegression().fit(X_train, y_train)
pred_prob = logreg.predict_proba(X_test)
pred = [1 if i[1] >= 0.49 else 0 for i in pred_prob]
acc = accuracy_score(y_test, pred)
print(acc)

# CV - LogReg & Random Forest
'''
cv_results = cross_validate(logreg, X, y, cv=5, return_train_score=False)
print(cv_results['test_score'])
randomforest = RandomForestClassifier(10, max_depth=15)
cv_results = cross_validate(randomforest, X, y, cv=5, return_train_score=False)
print(cv_results['test_score'])
'''