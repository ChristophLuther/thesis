# Naive Bayes Classifier
from sklearn.naive_bayes import MultinomialNB
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split


# TODO fit models separately for all data

# read data
data_file = "sachs_s"
df = pd.read_csv(f"data/sachs/{data_file}.csv")

# prepare data for model
mapping_rf = {"LOW": 0, "AVG": 1, "HIGH": 2}
col_names = df.columns.tolist()
for i in col_names:
    df[i] = df.replace({i: mapping_rf})[i]
X = df[col_names[1:]]
y = df["Akt"]

# split data for train and test purpose
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.1, random_state=42
)

# define model and fit to data
mnb = MultinomialNB()
mnb.fit(X_train, y_train)

# make model prediction (single values)
y_pred = mnb.predict(X_test)

# make model prediction (vectors of probabilities; NOT to be interpreted)
probs = mnb.predict_proba(X_test)


# save model
filename = f"fitted_models/mnb/{data_file}.sav"
pickle.dump(mnb, open(filename, "wb"))
