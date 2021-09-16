# full experiment to compare SAGE vs CG SAGE (in original implementation by Covert et al.)

import sage
import pickle
import pandas as pd
from time import time
from sklearn.model_selection import train_test_split
import mlflow

# to loop through models
models = ["lm", "rfReg"]

# loop through graphs (true and estimated - with 'best' method); we input the adjacency matrix
graphs = ["dag_s", "dag_m", "dag_l"]

for graph in graphs:
    df = pd.read_csv(f"data/{graph}/{graph}_10000_obs.csv")
    col_names = df.columns.to_list()
    col_names.remove("V1")
    X = df[col_names]
    y = df["V1"]
    # split data for train and test purpose
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.1, random_state=42
    )

    X_train = X_train.to_numpy()
    X_test = X_test.to_numpy()
    y_train = y_train.to_numpy()
    y_test = y_test.to_numpy()

    adj_mat = pickle.load(open(f"results_py/true_amat/{graph}_10000_obs.p", "rb"))
    for model in models:
        fitted_model = pickle.load(open(f"fitted_models/{graph}_{model}.sav", "rb"))
        # SAGE according to covert
        imputer = sage.MarginalImputer(model, X_train)
        estimator = sage.PermutationEstimator(imputer, "mse")
        cg_estimator = sage.PermutationEstimator(imputer, "mse", dsep_test=True,
                                                 adj_mat=adj_mat, col_names=col_names, target='V1')

        # sage values
        start_time = time()
        sage_values = estimator(X_test, y_test)
        time_og = time() - start_time

        # cg values
        start_time_cg = time()
        cg_values = cg_estimator(X_test, y_test)
        time_cg = time() - start_time_cg
