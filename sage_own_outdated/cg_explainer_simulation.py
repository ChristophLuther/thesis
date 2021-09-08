# first draft:  file for simulation of different SAGE approaches with a given model,
# given data, given graph (fix cost for graph are subtracted later)

import pandas as pd
import pickle
from own_sage import CGsage
from sklearn.model_selection import train_test_split
from sklearn.metrics import log_loss
# data 

df = pd.read_csv('data/survey/survey_s_num.csv')
col_names = df.columns.to_list()
col_names.remove("T")
X = df[col_names]
y = df["T"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

# graph (adjacency matrix)
adj_mat = pickle.load(open("true_amat_py/survey.p", "rb"))


