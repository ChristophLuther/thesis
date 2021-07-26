# Random Forest Classifier
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


# read data
df = pd.read_csv("data/csv/sachs.csv")

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

# define model
rf = RandomForestClassifier(n_estimators=2000, random_state=42)

# fit model to data
rf.fit(X_train, y_train)

# make model prediction (single values)
y_pred = rf.predict(X_test)

# make model prediction (vectors of probabilities)
probs = rf.predict_proba(X_test)

# print("Accuracy:", metrics.accuracy_score(y_test, y_pred))

# save model
filename = "models/rf.sav"
pickle.dump(rf, open(filename, "wb"))
