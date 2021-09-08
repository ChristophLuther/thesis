"""Fit naive Bayes classifiers for every discrete data set
    n = 10,000 split in 90:10"""
from sklearn.naive_bayes import MultinomialNB
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split


# TODO what sample size for model fitting (we do not care abouot performance, but we still require the properties): m
names = ["asia", "alarm", "sachs", "hepar"]
# read data
for i in names:
    df = pd.read_csv(f"data/{i}/{i}_s_num.csv")
    if i == "asia":
        col_names = df.columns.tolist()
        col_names.remove("dysp")
        X = df[col_names]
        y = df["dysp"]
    elif i == "alarm":
        col_names = df.columns.tolist()
        col_names.remove("CATECHOL")
        X = df[col_names]
        y = df["CATECHOL"]
    elif i == "sachs":
        col_names = df.columns.tolist()
        col_names.remove("Akt")
        X = df[col_names]
        y = df["Akt"]
    else:
        col_names = df.columns.tolist()
        col_names.remove("Cirrhosis")
        X = df[col_names]
        y = df["Cirrhosis"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.1, random_state=42
    )

    mnb = MultinomialNB()
    mnb.fit(X_train, y_train)
    if i == "asia":
        filename = f"fitted_models/mnb/asia_s.sav"
        pickle.dump(mnb, open(filename, "wb"))
    elif i == "sachs":
        filename = f"fitted_models/mnb/sachs_s.sav"
        pickle.dump(mnb, open(filename, "wb"))
    elif i == "alarm":
        filename = f"fitted_models/mnb/alarm_s.sav"
        pickle.dump(mnb, open(filename, "wb"))
    else:
        filename = f"fitted_models/mnb/hepar_s.sav"
        pickle.dump(mnb, open(filename, "wb"))
