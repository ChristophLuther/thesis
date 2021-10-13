"""Plot SAGE values and their differences to SAGE_CG and SAGE_CG_CD"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import math


# Functions from utils file of rfi.plots
def coord_height_to_pixels(ax, height):
    p1 = ax.transData.transform((0, height))
    p2 = ax.transData.transform((0, 0))

    pix_height = p1[1] - p2[1]
    return pix_height


def hbar_text_position(rect, x_pos=0.5, y_pos=0.5):
    rx, ry = rect.get_xy()
    width = rect.get_width()
    height = rect.get_height()

    tx = rx + (width * x_pos)
    ty = ry + (height * y_pos)
    return (tx, ty)


def fi_hbarplot(ex, textformat='{:5.2f}', ax=None, figsize=None):
    """
    Function that plots the result of an RFI computation as a barplot
    Args:
        figsize:
        ax:
        textformat:
        ex: Explanation object
    """

    names = diff_sage_cg.index
    rfis = ex['mean'].to_numpy()
    stds = ex['std'].to_numpy()

    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)

    ixs = np.arange(rfis.shape[0] + 0.5, 0.5, -1)

    ax.barh(ixs, rfis, tick_label=names, xerr=stds, capsize=5, color=['mistyrose',
                                                                      'salmon', 'tomato',
                                                                      'darksalmon', 'coral'])
    # color = ['lightcoral',
    #          'moccasin', 'darkseagreen',
    #          'paleturquoise', 'lightsteelblue']
    return ax

# for latex font
plt.rc('text', usetex=True)
plt.rc('font', family='serif')


# data, model
datasets = ["asia", "asia", "asia", "asia"]
model = "cnb"

# Was habe ich an data? sage vals, sage_cg, sage_cg_est, sage_cg_cd, sage_cg_cd_est
# was will ich für einen plot? 5x3: obere reihe sage values für dags s m l
# darunter die diffs sage - sage_cg, - sage_cg_est, - sage_cg_cd, -sage_cg_cd_est
# dafür nehme ich die data über die runs, damit ich wenigstens n bisschen variance plotten kann

# initiate plot, fill it in for loop
fig, ax = plt.subplots(4, 3, figsize=(8, 8))
fig.tight_layout(pad=2.1)
ax[0, 0].set_title('SAGE')
ax[0, 1].set_title('SAGE$_{cg}$')
ax[0, 2].set_title('SAGE$_{cg}^{*}$')

# load data
for i in range(4):
    data = datasets[i]

    og_data = pd.read_csv(f"data/{data}.csv")
    col_names = og_data.columns.tolist()

    # load the 5 runs
    sage_0 = pd.read_csv(f"results/discrete/{data}/sage_{data}_{model}_0.csv")
    sage_1 = pd.read_csv(f"results/discrete/{data}/sage_{data}_{model}_1.csv")
    sage_2 = pd.read_csv(f"results/discrete/{data}/sage_{data}_{model}_2.csv")
    sage_3 = pd.read_csv(f"results/discrete/{data}/sage_{data}_{model}_3.csv")
    sage_4 = pd.read_csv(f"results/discrete/{data}/sage_{data}_{model}_4.csv")

    # get top 5
    sage = abs(sage_0)
    sage = sage.sort_values(ascending=False, by="0")
    sage = sage.iloc[0:5]
    top_five = []
    for ii in range(5):
        top_five.append(sage.index[ii])

    labels = []
    for ii in range(5):
        labels.append(col_names[top_five[ii]])

    # load the other data
    cg_0 = pd.read_csv(f"results/discrete/{data}/cg_{data}_{model}_0.csv")
    cg_1 = pd.read_csv(f"results/discrete/{data}/cg_{data}_{model}_1.csv")
    cg_2 = pd.read_csv(f"results/discrete/{data}/cg_{data}_{model}_2.csv")
    cg_3 = pd.read_csv(f"results/discrete/{data}/cg_{data}_{model}_3.csv")
    cg_4 = pd.read_csv(f"results/discrete/{data}/cg_{data}_{model}_4.csv")

    # load the other data
    cg_est_0 = pd.read_csv(f"results/discrete/{data}/cg_est_{data}_{model}_0.csv")
    cg_est_1 = pd.read_csv(f"results/discrete/{data}/cg_est_{data}_{model}_1.csv")
    cg_est_2 = pd.read_csv(f"results/discrete/{data}/cg_est_{data}_{model}_2.csv")
    cg_est_3 = pd.read_csv(f"results/discrete/{data}/cg_est_{data}_{model}_3.csv")
    cg_est_4 = pd.read_csv(f"results/discrete/{data}/cg_est_{data}_{model}_4.csv")

    sage_0 = sage_0.iloc[top_five, :]
    sage_1 = sage_1.iloc[top_five, :]
    sage_2 = sage_2.iloc[top_five, :]
    sage_3 = sage_3.iloc[top_five, :]
    sage_4 = sage_4.iloc[top_five, :]
    cg_0 = cg_0.iloc[top_five, :]
    cg_1 = cg_1.iloc[top_five, :]
    cg_2 = cg_2.iloc[top_five, :]
    cg_3 = cg_3.iloc[top_five, :]
    cg_4 = cg_4.iloc[top_five, :]
    cg_est_0 = cg_est_0.iloc[top_five, :]
    cg_est_1 = cg_est_1.iloc[top_five, :]
    cg_est_2 = cg_est_2.iloc[top_five, :]
    cg_est_3 = cg_est_3.iloc[top_five, :]
    cg_est_4 = cg_est_4.iloc[top_five, :]

    # differences
    sage_cg_0 = sage_0 - cg_0
    sage_cg_1 = sage_1 - cg_1
    sage_cg_2 = sage_2 - cg_2
    sage_cg_3 = sage_3 - cg_3
    sage_cg_4 = sage_4 - cg_4
    sage_cg_est_0 = sage_0 - cg_est_0
    sage_cg_est_1 = sage_1 - cg_est_1
    sage_cg_est_2 = sage_2 - cg_est_2
    sage_cg_est_3 = sage_3 - cg_est_3
    sage_cg_est_4 = sage_4 - cg_est_4


    SAGE = pd.DataFrame(columns=labels)
    SAGE.loc[0] = np.array(sage_0["0"])
    SAGE.loc[1] = np.array(sage_1["0"])
    SAGE.loc[2] = np.array(sage_2["0"])
    SAGE.loc[3] = np.array(sage_3["0"])
    SAGE.loc[4] = np.array(sage_4["0"])

    SAGE_CG = pd.DataFrame(columns=labels)
    SAGE_CG.loc[0] = np.array(sage_cg_0["0"])
    SAGE_CG.loc[1] = np.array(sage_cg_1["0"])
    SAGE_CG.loc[2] = np.array(sage_cg_2["0"])
    SAGE_CG.loc[3] = np.array(sage_cg_3["0"])
    SAGE_CG.loc[4] = np.array(sage_cg_4["0"])

    SAGE_CG_EST = pd.DataFrame(columns=labels)
    SAGE_CG_EST.loc[0] = np.array(sage_cg_est_0["0"])
    SAGE_CG_EST.loc[1] = np.array(sage_cg_est_1["0"])
    SAGE_CG_EST.loc[2] = np.array(sage_cg_est_2["0"])
    SAGE_CG_EST.loc[3] = np.array(sage_cg_est_3["0"])
    SAGE_CG_EST.loc[4] = np.array(sage_cg_est_4["0"])

    sage_fi = pd.DataFrame(SAGE.mean(), columns=['mean'])
    sage_fi['std'] = SAGE.std()
    diff_sage_cg = pd.DataFrame(SAGE_CG.mean(), columns=['mean'])
    diff_sage_cg['std'] = SAGE_CG.std()
    diff_sage_cg_est = pd.DataFrame(SAGE_CG_EST.mean(), columns=['mean'])
    diff_sage_cg_est['std'] = SAGE_CG_EST.std()

    # plots
    fi_hbarplot(sage_fi, ax=ax[i, 0])
    fi_hbarplot(diff_sage_cg, ax=ax[i, 1])
    fi_hbarplot(diff_sage_cg_est, ax=ax[i, 2])

ax[0, 0].set_ylabel('Asia')
ax[1, 0].set_ylabel('Sachs')
ax[2, 0].set_ylabel('Alarm')
ax[3, 0].set_ylabel('Hepar II')

plt.savefig(f"results/plots/sage_vales_{model}.png", dpi=400, bbox_inches='tight')

