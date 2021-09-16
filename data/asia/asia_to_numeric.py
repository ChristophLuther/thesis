import pandas as pd
filenames = ["asia_s", "asia_m", "asia_l", "asia_xl", "asia_train", "asia_test"]

for filename in filenames:
    df = pd.read_csv(f"data/asia/{filename}.csv")
    mapping_rf = {"no": 0, "yes": 1}
    col_names = df.columns.tolist()
    for i in col_names:
        df[i] = df.replace({i: mapping_rf})[i]

    df.to_csv(f"data/asia/{filename}.csv", index=False)
