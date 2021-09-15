"""Fit linear model to data, simple template used in CG SAGE project"""
from sklearn.linear_model import LinearRegression
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
import sys
import os
import inspect


current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


from functions import create_folder

# create folder to store models
create_folder(".fitted_models/")

names = ["dag_s", "dag_m", "dag_l", "dag_xl"]

# read data
for i in names:

    df = pd.read_csv(f"data/{i}/{i}_train.csv")
    col_names = df.columns.tolist()
    # We use "x1" as target, since we randomly sampled edges, this is w.l.o.g. a target at a random
    # position in the graph
    col_names.remove("x1")
    X = df[col_names]
    y = df["x1"]

    # standard train test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.1, random_state=42
    )

    # fit model
    lm = LinearRegression()
    lm.fit(X_train, y_train)

    # save model
    filename = f"fitted_models/{i}_lm.sav"
    pickle.dump(lm, open(filename, "wb"))
