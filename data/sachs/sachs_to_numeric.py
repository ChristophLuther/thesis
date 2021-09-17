import pandas as pd
filenames = ["sachs_s", "sachs_l", "sachs_xl", "sachs_train", "sachs_test"]

for filename in filenames:
    df = pd.read_csv(f"data/sachs/{filename}.csv")
    mapping_rf = {"LOW": 0, "AVG": 1,  "HIGH": 2}
    col_names = df.columns.tolist()
    for i in col_names:
        df[i] = df.replace({i: mapping_rf})[i]

    df.to_csv(f"data/sachs/{filename}.csv", index=False)
