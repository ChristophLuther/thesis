"""
Experiment file for CGExplainer with discrete DAGs (adapted from SAGE according to Covert (2020)

Command line args:
    --data CSV file in folder ~/data/ (string without suffix)
    --model choice between categorical naive Bayes ('cnb') and random forest classification ('rf')
    --size slice dataset to df[0:size] (int)
    --thresh threshold for convergence detection
    --split for train test split
    --target target of the model
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import CategoricalNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import sage
import pickle
import time
import argparse


parser = argparse.ArgumentParser(
    description="Experiment to compare SAGE estimation with and without d-separation tests")

parser.add_argument(
    "-d",
    "--data",
    type=str,
    default="asia",
    help="What data to use?")


parser.add_argument(
    "-m",
    "--model",
    type=str,
    default="cnb",
    help="categorical naive Bayes ('cnb') or random forest classification ('rf')?",
)

parser.add_argument(
    "-n",
    "--size",
    type=int,
    default=None,
    help="Custom sample size to slice df",
)


parser.add_argument(
    "-t",
    "--thresh",
    type=float,
    default=0.025,
    help="Threshold for convergence detection",
)

parser.add_argument(
    "-s",
    "--split",
    type=float,
    default=0.2,
    help="Train test split",
)

parser.add_argument(
    "-y",
    "--target",
    type=str,
    default="dysp",
    help="Target node of models",
)

arguments = parser.parse_args()

# seed
np.random.seed(1902)


def main(args):
    # define target directory
    savepath = f"sage_covert/results/discrete/{args.data}"
    # df to store some metadata
    col_names_meta = ["data", "model", "runtime sage", "runtime cg", "runtime cg est"]
    metadata = pd.DataFrame(columns=col_names_meta)

    # import and prepare data
    df = pd.read_csv(f"sage_covert/data/{args.data}.csv")
    if args.size is not None:
        df = df[0:args.size]
    col_names = df.columns.tolist()
    col_names.remove(args.target)
    X = df[col_names]
    y = df[args.target]

    # split data for train and test purpose
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=args.split, random_state=42
    )

    # initiate df for details of models
    col_names_model = ["data", "model", "target", "accuracy"]
    model_details = pd.DataFrame(columns=col_names_model)

    # fit model
    if args.model == "cnb":
        # fit model
        model = CategoricalNB()
        model.fit(X_train, y_train)
        # model evaluation
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        # fill df with info about model
        model_details.loc[len(model_details)] = [args.data, "cnb", args.target, acc]
        model_details.to_csv(
            f"{savepath}/model_details_cnb.csv", index=False
        )
    else:
        # fit model
        model = RandomForestClassifier(n_estimators=100)
        model.fit(X_train, y_train)
        # model evaluation
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        # fill df with info about model
        model_details.loc[len(model_details)] = [args.data, "rf cf", args.target, acc]
        model_details.to_csv(
            f"{savepath}/model_details_rf.csv", index=False
        )

    X_train = X_train.to_numpy()
    X_test = X_test.to_numpy()
    y_train = y_train.to_numpy()
    y_test = y_test.to_numpy()

    # load adjacency matrices for CGExplainer
    amat_true = pickle.load(open(f"sage_covert/data/{args.data}.p", "rb"))
    amat_est = pickle.load(open(f"sage_covert/data/{args.data}_est.p", "rb"))

    # set up imputer (same for all Estimators)
    imputer = sage.MarginalImputer(model, X_train)

    # set seed before every estimator to ensure consistent results
    np.random.seed(1902)

    # Explainer
    estimator = sage.PermutationEstimator(imputer, "cross entropy", track_deltas=True, col_names=col_names)

    # track time with time module
    time_sage = 0
    sage_i = 0
    while sage_i < 5:
        start_time = time.time()
        sage_values, deltas = estimator(X_test, y_test)
        time_sage = (time.time() - start_time) + time_sage
        pd.DataFrame(sage_values.values).to_csv(f"{savepath}/sage_{args.data}_{args.model}_{sage_i}.csv")
        deltas.to_csv(f"{savepath}/deltas_{args.data}_{args.model}_{sage_i}.csv")
        sage_i += 1

    # CGExplainer
    np.random.seed(1902)
    cg_estimator = sage.PermutationEstimator(imputer, "cross entropy", dsep_test=True, track_deltas=True,
                                             adj_mat=amat_true, col_names=col_names, target=args.target)

    # CG Sage run with same orderings as SAGE run (ensured by seed)
    time_cg = 0
    cg_i = 0
    while cg_i < 5:
        start_time_cg = time.time()
        cg_values, cg_deltas = cg_estimator(X_test, y_test)
        time_cg = (time.time() - start_time_cg) + time_cg
        pd.DataFrame(cg_values.values).to_csv(f"{savepath}/cg_{args.data}_{args.model}_{cg_i}.csv")
        cg_deltas.to_csv(f"{savepath}/deltas_cg_{args.data}_{args.model}_{cg_i}.csv")
        cg_i += 1

    # CGExplainer (with estimated amat)
    np.random.seed(1902)
    cg_est_estimator = sage.PermutationEstimator(imputer, "cross entropy", dsep_test=True, track_deltas=True,
                                                 adj_mat=amat_est, col_names=col_names, target=args.target)

    # CG Sage run with same orderings as SAGE run
    time_cg_est = 0
    cg_est_i = 0
    while cg_est_i < 5:
        start_time_cg_est = time.time()
        cg_est_values, cg_est_deltas = cg_est_estimator(X_test, y_test)
        time_cg_est = (time.time() - start_time_cg_est) + time_cg_est
        pd.DataFrame(cg_est_values.values).to_csv(f"{savepath}/cg_est_{args.data}_{args.model}_{cg_est_i}.csv")
        cg_est_deltas.to_csv(f"{savepath}/deltas_cg_est_{args.data}_{args.model}_{cg_est_i}.csv")
        cg_est_i += 1

    content = [args.data, args.model, time_sage, time_cg, time_cg_est]
    # fill evaluation table with current run
    metadata.loc[len(metadata)] = content
    metadata.to_csv(f"{savepath}/metadata_{args.data}_{args.model}.csv", index=False)


if __name__ == "__main__":
    main(arguments)
