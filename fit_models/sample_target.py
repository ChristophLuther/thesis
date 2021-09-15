"""Sample targets for the Alarm and Sachs data"""

import pandas as pd
import random

random.seed(1902)

# read data

df_alarm = pd.read_csv("data/alarm/alarm_s.csv")
df_sachs = pd.read_csv("data/sachs/sachs_s.csv")

# randomly draw target from column names
target_alarm = random.choice(df_alarm.columns.to_list())
sachs_targets = df_sachs.columns.to_list()

for i in ["Akt", "PKC", "Plcg", "P38", "PIP2", "PIP3"]:
    sachs_targets.remove(i)

target_sachs = random.choice(sachs_targets)

print(target_alarm)
print(target_sachs)
