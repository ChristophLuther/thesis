"""Fit multinomial Bayes classifier to data, simple template used in CG SAGE project"""
from sklearn.naive_bayes import MultinomialNB
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

names = ["asia", "alarm", "sachs", "hepar"]

for i in names:
    # read data
    df = pd.read_csv(f"data/{i}/{i}_train.csv")
    if i == "asia":
        col_names = df.columns.tolist()
        col_names.remove("dysp")
        X = df[col_names]
        y = df["dysp"]
    elif i == "alarm":
        col_names = df.columns.tolist()
        col_names.remove("CVP")
        X = df[col_names]
        y = df["CVP"]
    elif i == "sachs":
        col_names = df.columns.tolist()
        col_names.remove("Erk")
        X = df[col_names]
        y = df["Erk"]
    else:
        col_names = df.columns.tolist()
        col_names.remove("Cirrhosis")
        X = df[col_names]
        y = df["Cirrhosis"]

    # standard train test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.1, random_state=42
    )

    # fit model
    mnb = MultinomialNB()
    mnb.fit(X_train, y_train)

    # save model
    filename = f"fitted_models/{i}_mnb.sav"
    pickle.dump(mnb, open(filename, "wb"))
