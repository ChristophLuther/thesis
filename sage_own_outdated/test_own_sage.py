import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import log_loss
from own_sage import CGsage

df = pd.read_csv("data/survey/survey_s_num.csv")
clf = pickle.load(open("fitted_models/rf/survey_s_est20.sav", "rb"))
adj_mat = pickle.load(open("true_amat_py/survey.p", "rb"))
col_namez = df.columns.to_list()
col_namez.remove("T")
X = df[col_namez]
y = df["T"]
# split data for train and test purpose
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.1, random_state=42
)

wrk = CGsage(X_test, y_test,clf, log_loss, X_train)
values = wrk.sage_fn()
print(values)

