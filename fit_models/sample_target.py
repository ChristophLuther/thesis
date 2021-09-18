"""Sample targets for the Alarm and Sachs data"""

import pandas as pd
import random

random.seed(1902)

# read data

df_sachs = pd.read_csv("data/sachs/sachs_s.csv")

# randomly draw target from column names
sachs_targets = df_sachs.columns.to_list()

for i in ["Akt", "PKC", "Plcg", "P38", "PIP2", "PIP3"]:
    sachs_targets.remove(i)

target_sachs = random.choice(sachs_targets)

print(target_sachs)
