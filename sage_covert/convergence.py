"""Plot convergence behaviour of """
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import pandas as pd
import numpy as np


# for latex font
plt.rc('text', usetex=True)
plt.rc('font', family='serif')


# data, model
datasets = ["asia", "asia", "asia", "asia"]
model = "cnb"

# initiate plot, fill it in for loop
fig, ax = plt.subplots(4, 3, figsize=(12, 15))
fig.tight_layout(pad=1.8)
ax[0, 0].set_title('SAGE')
ax[0, 1].set_title('SAGE$_{cg}$')
ax[0, 2].set_title('SAGE$_{cg}^*$')

# load data
for i in range(4):
    # TODO: retrieve  5 largest sage values, use their index to get name from col
    # TODO (ctd) name, use these 5 col names,  to get deltas_0_colname, plot convergence lol!
    data = datasets[i]
    og_data = pd.read_csv(f"data/{data}.csv")
    col_names = og_data.columns.tolist()
    # first retrieve the normal sage values from the first run to determine the five largest
    sage = pd.read_csv(f"results/discrete/{data}/sage_{data}_{model}_0.csv")
    sage = sage["0"]
    sage = abs(sage)
    sage = sage.sort_values(ascending=False)
    sage = sage.iloc[0:5]
    top_five = []
    for ii in range(5):
        top_five.append(sage.index[ii])

    deltas_0 = pd.read_csv(f"results/discrete/{data}/deltas_{data}_{model}_0.csv")
    deltas_0_1 = deltas_0[deltas_0["foi"] == col_names[top_five[0]]]
    deltas_0_2 = deltas_0[deltas_0["foi"] == col_names[top_five[1]]]
    deltas_0_3 = deltas_0[deltas_0["foi"] == col_names[top_five[2]]]
    deltas_0_4 = deltas_0[deltas_0["foi"] == col_names[top_five[3]]]
    deltas_0_5 = deltas_0[deltas_0["foi"] == col_names[top_five[4]]]

    deltas_0_1 = deltas_0_1["deltas"]
    for k in range(len(deltas_0_1)):
        deltas_0_1.iloc[k] = float(deltas_0_1.iloc[k][1:-1])

    deltas_0_2 = deltas_0_2["deltas"]
    for k in range(len(deltas_0_2)):
        deltas_0_2.iloc[k] = float(deltas_0_2.iloc[k][1:-1])

    deltas_0_3 = deltas_0_3["deltas"]
    for k in range(len(deltas_0_3)):
        deltas_0_3.iloc[k] = float(deltas_0_3.iloc[k][1:-1])

    deltas_0_4 = deltas_0_4["deltas"]
    for k in range(len(deltas_0_4)):
        deltas_0_4.iloc[k] = float(deltas_0_4.iloc[k][1:-1])

    deltas_0_5 = deltas_0_5["deltas"]
    for k in range(len(deltas_0_5)):
        deltas_0_5.iloc[k] = float(deltas_0_5.iloc[k][1:-1])


    deltas_cg_0 = pd.read_csv(f"results/discrete/{data}/deltas_cg_{data}_{model}_0.csv")
    deltas_cg_0_1 = deltas_cg_0[deltas_cg_0["foi"] == col_names[top_five[0]]]
    deltas_cg_0_2 = deltas_cg_0[deltas_cg_0["foi"] == col_names[top_five[1]]]
    deltas_cg_0_3 = deltas_cg_0[deltas_cg_0["foi"] == col_names[top_five[2]]]
    deltas_cg_0_4 = deltas_cg_0[deltas_cg_0["foi"] == col_names[top_five[3]]]
    deltas_cg_0_5 = deltas_cg_0[deltas_cg_0["foi"] == col_names[top_five[4]]]

    deltas_cg_0_1 = deltas_cg_0_1["deltas"]
    for k in range(len(deltas_cg_0_1)):
        try:
            deltas_cg_0_1.iloc[k] = float(deltas_cg_0_1.iloc[k])
        except:
            deltas_cg_0_1.iloc[k] = float(deltas_cg_0_1.iloc[k][1:-1])

    deltas_cg_0_2 = deltas_cg_0_2["deltas"]
    for k in range(len(deltas_cg_0_2)):
        try:
            deltas_cg_0_2.iloc[k] = float(deltas_cg_0_2.iloc[k])
        except:
            deltas_cg_0_2.iloc[k] = float(deltas_cg_0_2.iloc[k][1:-1])

    deltas_cg_0_3 = deltas_cg_0_3["deltas"]
    for k in range(len(deltas_cg_0_3)):
        try:
            deltas_cg_0_3.iloc[k] = float(deltas_cg_0_3.iloc[k])
        except:
            deltas_cg_0_3.iloc[k] = float(deltas_cg_0_3.iloc[k][1:-1])

    deltas_cg_0_4 = deltas_cg_0_4["deltas"]
    for k in range(len(deltas_cg_0_4)):
        try:
            deltas_cg_0_4.iloc[k] = float(deltas_cg_0_4.iloc[k])
        except:
            deltas_cg_0_4.iloc[k] = float(deltas_cg_0_4.iloc[k][1:-1])

    deltas_cg_0_5 = deltas_cg_0_5["deltas"]
    for k in range(len(deltas_cg_0_5)):
        try:
            deltas_cg_0_5.iloc[k] = float(deltas_cg_0_5.iloc[k])
        except:
            deltas_cg_0_5.iloc[k] = float(deltas_cg_0_5.iloc[k][1:-1])

    deltas_cg_est_0 = pd.read_csv(f"results/discrete/{data}/deltas_cg_est_{data}_{model}_0.csv")
    deltas_cg_est_0_1 = deltas_cg_est_0[deltas_cg_est_0["foi"] == col_names[top_five[0]]]
    deltas_cg_est_0_2 = deltas_cg_est_0[deltas_cg_est_0["foi"] == col_names[top_five[1]]]
    deltas_cg_est_0_3 = deltas_cg_est_0[deltas_cg_est_0["foi"] == col_names[top_five[2]]]
    deltas_cg_est_0_4 = deltas_cg_est_0[deltas_cg_est_0["foi"] == col_names[top_five[3]]]
    deltas_cg_est_0_5 = deltas_cg_est_0[deltas_cg_est_0["foi"] == col_names[top_five[4]]]

    deltas_cg_est_0_1 = deltas_cg_est_0_1["deltas"]
    for k in range(len(deltas_cg_est_0_1)):
        try:
            deltas_cg_est_0_1.iloc[k] = float(deltas_cg_est_0_1.iloc[k])
        except:
            deltas_cg_est_0_1.iloc[k] = float(deltas_cg_est_0_1.iloc[k][1:-1])

    deltas_cg_est_0_2 = deltas_cg_est_0_2["deltas"]
    for k in range(len(deltas_cg_est_0_2)):
        try:
            deltas_cg_est_0_2.iloc[k] = float(deltas_cg_est_0_2.iloc[k])
        except:
            deltas_cg_est_0_2.iloc[k] = float(deltas_cg_est_0_2.iloc[k][1:-1])

    deltas_cg_est_0_3 = deltas_cg_est_0_3["deltas"]
    for k in range(len(deltas_cg_est_0_3)):
        try:
            deltas_cg_est_0_3.iloc[k] = float(deltas_cg_est_0_3.iloc[k])
        except:
            deltas_cg_est_0_3.iloc[k] = float(deltas_cg_est_0_3.iloc[k][1:-1])

    deltas_cg_est_0_4 = deltas_cg_est_0_4["deltas"]
    for k in range(len(deltas_cg_est_0_4)):
        try:
            deltas_cg_est_0_4.iloc[k] = float(deltas_cg_est_0_4.iloc[k])
        except:
            deltas_cg_est_0_4.iloc[k] = float(deltas_cg_est_0_4.iloc[k][1:-1])

    deltas_cg_est_0_5 = deltas_cg_est_0_5["deltas"]
    for k in range(len(deltas_cg_est_0_5)):
        try:
            deltas_cg_est_0_5.iloc[k] = float(deltas_cg_est_0_5.iloc[k])
        except:
            deltas_cg_est_0_5.iloc[k] = float(deltas_cg_est_0_5.iloc[k][1:-1])

    DELTAS_1 = np.array(deltas_0_1)
    DELTAS_2 = np.array(deltas_0_2)
    DELTAS_3 = np.array(deltas_0_3)
    DELTAS_4 = np.array(deltas_0_4)
    DELTAS_5 = np.array(deltas_0_5)

    DELTAS_CG_1 = np.array(deltas_cg_0_1)
    DELTAS_CG_2 = np.array(deltas_cg_0_2)
    DELTAS_CG_3 = np.array(deltas_cg_0_3)
    DELTAS_CG_4 = np.array(deltas_cg_0_4)
    DELTAS_CG_5 = np.array(deltas_cg_0_5)

    DELTAS_CG_EST_1 = np.array(deltas_cg_est_0_1)
    DELTAS_CG_EST_2 = np.array(deltas_cg_est_0_2)
    DELTAS_CG_EST_3 = np.array(deltas_cg_est_0_3)
    DELTAS_CG_EST_4 = np.array(deltas_cg_est_0_4)
    DELTAS_CG_EST_5 = np.array(deltas_cg_est_0_5)

    DELTAS = pd.DataFrame()
    DELTAS[col_names[top_five[0]]] = DELTAS_1
    DELTAS[col_names[top_five[1]]] = DELTAS_2
    DELTAS[col_names[top_five[2]]] = DELTAS_3
    DELTAS[col_names[top_five[3]]] = DELTAS_4
    DELTAS[col_names[top_five[4]]] = DELTAS_5

    DELTAS_CG = pd.DataFrame()
    DELTAS_CG[col_names[top_five[0]]] = DELTAS_CG_1
    DELTAS_CG[col_names[top_five[1]]] = DELTAS_CG_2
    DELTAS_CG[col_names[top_five[2]]] = DELTAS_CG_3
    DELTAS_CG[col_names[top_five[3]]] = DELTAS_CG_4
    DELTAS_CG[col_names[top_five[4]]] = DELTAS_CG_5

    DELTAS_CG_EST = pd.DataFrame()
    DELTAS_CG_EST[col_names[top_five[0]]] = DELTAS_CG_EST_1
    DELTAS_CG_EST[col_names[top_five[1]]] = DELTAS_CG_EST_2
    DELTAS_CG_EST[col_names[top_five[2]]] = DELTAS_CG_EST_3
    DELTAS_CG_EST[col_names[top_five[3]]] = DELTAS_CG_EST_4
    DELTAS_CG_EST[col_names[top_five[4]]] = DELTAS_CG_EST_5

    # das ganze für sage cg  cg_cd cg_est cg_cd_est
    std_sage = pd.DataFrame(columns=DELTAS.columns)
    for j in range(2, len(DELTAS)):
        diffs = DELTAS[0:j + 1] - DELTAS[0:j + 1].mean()
        # squared differences
        diffs2 = diffs * diffs
        # sum of squared diffs
        diffs2_sum = diffs2.sum()
        # sum of diffs
        diffs_sum = diffs.sum()
        # diffs_sum2 = (diffs_sum * diffs_sum)
        # diffs_sum2_n = (diffs_sum2/ii)
        variance = (diffs2_sum - ((diffs_sum * diffs_sum) / j)) / (j - 1)
        std = variance ** 0.5
        std_sage.loc[j - 2] = std

    # get the means up to current ordering

    sage_running_mean = pd.DataFrame(columns=DELTAS.columns)
    for k in range(2, len(DELTAS)):
        sage_running_mean.loc[k] = DELTAS[0:k + 1].mean()

    sage_running_mean = sage_running_mean.reset_index(drop=True)

    # make confidence bands
    sage_lower = pd.DataFrame(columns=sage_running_mean.columns)
    sage_upper = pd.DataFrame(columns=sage_running_mean.columns)
    for ll in range(len(sage_running_mean)):
        sage_lower.loc[ll] = sage_running_mean.loc[ll] - 1.96 * (std_sage.loc[ll] / np.sqrt(ll + 3))
        sage_upper.loc[ll] = sage_running_mean.loc[ll] + 1.96 * (std_sage.loc[ll] / np.sqrt(ll + 3))

    x_sage = []
    for m in range(len(sage_running_mean)):
        x_sage.append(m)

    std_cg = pd.DataFrame(columns=DELTAS_CG.columns)
    for j in range(2, len(DELTAS_CG)):
        diffs = DELTAS_CG[0:j + 1] - DELTAS_CG[0:j + 1].mean()
        # squared differences
        diffs2 = diffs * diffs
        # sum of squared diffs
        diffs2_sum = diffs2.sum()
        # sum of diffs
        diffs_sum = diffs.sum()
        # diffs_sum2 = (diffs_sum * diffs_sum)
        # diffs_sum2_n = (diffs_sum2/ii)
        variance = (diffs2_sum - ((diffs_sum * diffs_sum) / j)) / (j - 1)
        std = variance ** 0.5
        std_cg.loc[j - 2] = std

    # get the means up to current ordering

    cg_running_mean = pd.DataFrame(columns=DELTAS_CG.columns)
    for k in range(2, len(DELTAS_CG)):
        cg_running_mean.loc[k] = DELTAS_CG[0:k + 1].mean()

    cg_running_mean = cg_running_mean.reset_index(drop=True)

    # make confidence bands
    cg_lower = pd.DataFrame(columns=cg_running_mean.columns)
    cg_upper = pd.DataFrame(columns=cg_running_mean.columns)
    for ll in range(len(cg_running_mean)):
        cg_lower.loc[ll] = cg_running_mean.loc[ll] - 1.96 * (std_cg.loc[ll] / np.sqrt(ll + 3))
        cg_upper.loc[ll] = cg_running_mean.loc[ll] + 1.96 * (std_cg.loc[ll] / np.sqrt(ll + 3))

    x_cg = []
    for m in range(len(cg_running_mean)):
        x_cg.append(m)

    std_cg_est = pd.DataFrame(columns=DELTAS_CG_EST.columns)
    for j in range(2, len(DELTAS_CG_EST)):
        diffs = DELTAS_CG_EST[0:j + 1] - DELTAS_CG_EST[0:j + 1].mean()
        # squared differences
        diffs2 = diffs * diffs
        # sum of squared diffs
        diffs2_sum = diffs2.sum()
        # sum of diffs
        diffs_sum = diffs.sum()
        # diffs_sum2 = (diffs_sum * diffs_sum)
        # diffs_sum2_n = (diffs_sum2/ii)
        variance = (diffs2_sum - ((diffs_sum * diffs_sum) / j)) / (j - 1)
        std = variance ** 0.5
        std_cg_est.loc[j - 2] = std

    # get the means up to current ordering

    cg_running_mean_est = pd.DataFrame(columns=DELTAS_CG_EST.columns)
    for k in range(2, len(DELTAS_CG_EST)):
        cg_running_mean_est.loc[k] = DELTAS_CG_EST[0:k + 1].mean()

    cg_running_mean_est = cg_running_mean_est.reset_index(drop=True)

    # make confidence bands
    cg_est_lower = pd.DataFrame(columns=cg_running_mean_est.columns)
    cg_est_upper = pd.DataFrame(columns=cg_running_mean_est.columns)
    for ll in range(len(cg_running_mean_est)):
        cg_est_lower.loc[ll] = cg_running_mean_est.loc[ll] - 1.96 * (std_cg_est.loc[ll] / np.sqrt(ll + 3))
        cg_est_upper.loc[ll] = cg_running_mean_est.loc[ll] + 1.96 * (std_cg_est.loc[ll] / np.sqrt(ll + 3))

    x_cg_est = []
    for m in range(len(cg_running_mean_est)):
        x_cg_est.append(m)

    ax[i, 0].plot(x_sage, sage_running_mean, linewidth=0.7)
    for n in sage_lower.columns:
        ax[i, 0].fill_between(x_sage, sage_lower[n], sage_upper[n], alpha=.1)

    ax[i, 1].plot(x_cg, cg_running_mean, linewidth=0.7)
    for n in cg_lower.columns:
        ax[i, 1].fill_between(x_cg, cg_lower[n], cg_upper[n], alpha=.1)

    ax[i, 2].plot(x_cg_est, cg_running_mean_est, linewidth=0.7)
    for n in cg_est_lower.columns:
        ax[i, 2].fill_between(x_cg_est, cg_est_lower[n], cg_est_upper[n], alpha=.1)

    ax[i, 2].legend(loc='upper right', labels=DELTAS_CG_EST.columns)

ax[3, 1].set_xlabel('No. of Permutations')
ax[0, 0].set_ylabel('Asia')
ax[1, 0].set_ylabel('Sachs')
ax[2, 0].set_ylabel('Alarm')
ax[3, 0].set_ylabel('Hepar II')

plt.savefig(f"results/plots/convergence_{model}.png", dpi=400, bbox_inches='tight')
