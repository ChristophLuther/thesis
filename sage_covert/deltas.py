"""Plot Confidence Intervals for the differences of the deltas between SAGE
and SAGE_CG if the is conditional independence

One confidence interval per experiment, confidence over nr_orderings"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# for latex font
plt.rc('text', usetex=True)
plt.rc('font', family='serif')


# data, model
datasets = ["asia", "asia", "asia", "asia", "asia", "asia", "asia", "asia"]
models = ["cnb", "rf", "cnb", "rf", "cnb", "rf",  "cnb", "rf"]
fig, ax = plt.subplots(1, 1, figsize=(4, 2.5))
est = False

for i in range(8):
    # load data
    data = datasets[i]
    model = models[i]
    deltas_0 = pd.read_csv(f"results/discrete/{data}/deltas_{data}_{model}_0.csv")
    deltas_1 = pd.read_csv(f"results/discrete/{data}/deltas_{data}_{model}_1.csv")
    deltas_2 = pd.read_csv(f"results/discrete/{data}/deltas_{data}_{model}_2.csv")
    deltas_3 = pd.read_csv(f"results/discrete/{data}/deltas_{data}_{model}_3.csv")
    deltas_4 = pd.read_csv(f"results/discrete/{data}/deltas_{data}_{model}_4.csv")

    if est is False:
        deltas_cg_0 = pd.read_csv(f"results/discrete/{data}/deltas_cg_{data}_{model}_0.csv")
        deltas_cg_1 = pd.read_csv(f"results/discrete/{data}/deltas_cg_{data}_{model}_1.csv")
        deltas_cg_2 = pd.read_csv(f"results/discrete/{data}/deltas_cg_{data}_{model}_2.csv")
        deltas_cg_3 = pd.read_csv(f"results/discrete/{data}/deltas_cg_{data}_{model}_3.csv")
        deltas_cg_4 = pd.read_csv(f"results/discrete/{data}/deltas_cg_{data}_{model}_4.csv")
    elif est is True:
        deltas_cg_0 = pd.read_csv(f"results/discrete/{data}/deltas_cg_est_{data}_{model}_0.csv")
        deltas_cg_1 = pd.read_csv(f"results/discrete/{data}/deltas_cg_est_{data}_{model}_1.csv")
        deltas_cg_2 = pd.read_csv(f"results/discrete/{data}/deltas_cg_est_{data}_{model}_2.csv")
        deltas_cg_3 = pd.read_csv(f"results/discrete/{data}/deltas_cg_est_{data}_{model}_3.csv")
        deltas_cg_4 = pd.read_csv(f"results/discrete/{data}/deltas_cg_est_{data}_{model}_4.csv")

    deltas_cg_0 = deltas_cg_0[deltas_cg_0["d-separated"] == True]
    deltas_cg_1 = deltas_cg_1[deltas_cg_1["d-separated"] == True]
    deltas_cg_2 = deltas_cg_2[deltas_cg_2["d-separated"] == True]
    deltas_cg_3 = deltas_cg_3[deltas_cg_3["d-separated"] == True]
    deltas_cg_4 = deltas_cg_4[deltas_cg_4["d-separated"] == True]

    index_0 = []
    for j in range(len(deltas_cg_0)):
        index_0.append(deltas_cg_0.index[j])
    index_1 = []
    for j in range(len(deltas_cg_1)):
        index_1.append(deltas_cg_1.index[j])
    index_2 = []
    for j in range(len(deltas_cg_2)):
        index_2.append(deltas_cg_2.index[j])
    index_3 = []
    for j in range(len(deltas_cg_3)):
        index_3.append(deltas_cg_3.index[j])
    index_4 = []
    for j in range(len(deltas_cg_4)):
        index_4.append(deltas_cg_4.index[j])

    deltas_0 = deltas_0.loc[index_0]["deltas"]
    deltas_1 = deltas_1.loc[index_1]["deltas"]
    deltas_2 = deltas_2.loc[index_2]["deltas"]
    deltas_3 = deltas_3.loc[index_3]["deltas"]
    deltas_4 = deltas_4.loc[index_4]["deltas"]

    for k in range(len(deltas_0)):
        deltas_0.iloc[k] = float(deltas_0.iloc[k][1:-1])
    for k in range(len(deltas_1)):
        deltas_1.iloc[k] = float(deltas_1.iloc[k][1:-1])
    for k in range(len(deltas_2)):
        deltas_2.iloc[k] = float(deltas_2.iloc[k][1:-1])
    for k in range(len(deltas_3)):
        deltas_3.iloc[k] = float(deltas_3.iloc[k][1:-1])
    for k in range(len(deltas_4)):
        deltas_4.iloc[k] = float(deltas_4.iloc[k][1:-1])

    DELTAS = np.concatenate((np.array(deltas_0), np.array(deltas_1), np.array(deltas_2),
                             np.array(deltas_3), np.array(deltas_4)))

    ci = 1.96 * np.std(DELTAS) / np.sqrt(len(DELTAS))
    mean = DELTAS.mean()
    lower = mean - ci
    upper = mean + ci

    # plot CIs
    plt.plot((lower, upper), (i + 1, i + 1), '-|', color='grey')
    plt.scatter(mean, i + 1, color='black', marker="|")

plt.yticks([1, 2, 3, 4, 5, 6, 7, 8], ["Asia (nb)", "Asia (rf)", "Sachs (nb)", "Sachs (rf)", "Alarm (nb)", "Alarm (rf)",
                                "Hepar II (nb)", "Hepar II (rf)"])
plt.subplots_adjust(left=0.3)


plt.vlines(0, 0, 8, colors='red', linestyles='--', linewidth=0.4)
plt.title(r"$\overline{\Delta_{sage}}$")
plt.savefig(f"results/plots/deltas_discrete_{est}.png", dpi=400, bbox_inches='tight')
plt.clf()
