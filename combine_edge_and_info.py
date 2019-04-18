import numpy as np
import pandas as pd

edge_data = pd.read_csv("edge_data.csv")

meta_data = pd.read_csv("amazon-meta.csv", encoding='latin1')

edge_data = edge_data.groupby(['source'], as_index=False)['target'].count()

joined_data = edge_data.merge(meta_data, how = 'inner', left_on = ['source'], right_on=['Id'])

joined_data.to_csv("Joined_data.csv")

