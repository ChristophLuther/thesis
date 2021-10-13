import sage
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
# import matplotlib.pyplot as plt
from time import time
import numpy as np


np.random.seed(1902)
# TODO track deltas and corresponding coalitions with mlflow
# load data and adjacency matrix
df = pd.read_csv("data/dag_s/dag_s_1000_obs.csv")
adj_mat = pickle.load(open("results_py/true_amat/dag_s.p", "rb"))

# load models
# mnb = pickle.load(open("fitted_models/mnb/sachs_m.sav", "rb"))
# rf = pickle.load(open("fitted_models/rf/sachs_m_est20.sav", "rb"))
lm = pickle.load(open("fitted_models/dag_s_lm.sav", "rb"))


col_names = df.columns.to_list()
col_names.remove("1")
X = df[col_names]
y = df["1"]

# split data for train and test purpose
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.1, random_state=42
)

X_train = X_train.to_numpy()
X_test = X_test.to_numpy()
y_train = y_train.to_numpy()
y_test = y_test.to_numpy()


models = [lm]

for model in models:
    # SAGE according to covert
    imputer = sage.MarginalImputer(model, X_train)
    estimator = sage.PermutationEstimator(imputer, "mse")
    cg_estimator = sage.PermutationEstimator(imputer, "mse", dsep_test=True,
                                             adj_mat=adj_mat, col_names=col_names, target='1')

    # sage values
    start_time = time()
    sage_values = estimator(X_train, y_train)
    time_og = time() - start_time

    # cg values
    start_time_cg = time()
    cg_values = cg_estimator(X_train, y_train)
    time_cg = time() - start_time_cg
