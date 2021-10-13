# full experiment to compare SAGE vs CG SAGE (in original implementation by Covert et al.)

import sage
import pickle
import pandas as pd
from time import time
from sklearn.model_selection import train_test_split
import numpy as np

# to loop through models
models = ["lm"]   # TODO all models that are fitted!

# to loop through graphs
graphs = ["dag_s"]  # TODO all graphs

for graph in graphs:
    # load data (not too many observations, see runtime warning len(X_train) > 1024)
    df = pd.read_csv(f"data/{graph}/{graph}_1000_obs.csv")  # decide on sample size

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

    # load adjacency matrix for
    true_amat = pickle.load(open(f"results_py/true_amat/{graph}.p", "rb"))
    # also load est amat (best one)
    # est_amat = pickle.load(open(f"results_py/true_amat/{graph}.p", "rb"))

    # to loop through amats
    amats = [true_amat]

    for model in models:
        np.random.seed(1902)
        # load model
        fitted_model = pickle.load(open(f"fitted_models/{graph}_{model}.sav", "rb"))
        # SAGE according to covert
        imputer = sage.MarginalImputer(fitted_model, X_train)
        estimator = sage.PermutationEstimator(imputer, "mse", track_deltas=True, col_names=col_names)
        # sage values
        start_time = time()
        sage_values, deltas = estimator(X_test, y_test)
        time_og = time() - start_time

        # TODO make graphs and and store result for normal SAGE here

        for adj_mat in amats:
            np.random.seed(1902)
            cg_estimator = sage.PermutationEstimator(imputer, "mse", dsep_test=True,
                                                     adj_mat=adj_mat, col_names=col_names, target='1',
                                                     track_deltas=True)

            # cg values
            start_time_cg = time()
            cg_values, delta_cg = cg_estimator(X_test, y_test)
            time_cg = time() - start_time_cg

            # TODO make graphs and store results in this loop
print(deltas.head())
print(delta_cg.head())
# TODO track convergence of SAGE in permutation estimator, also the deltas and the corresponding coalitions
# and make some nice plots