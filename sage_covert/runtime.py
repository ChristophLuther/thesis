import pandas as pd
import matplotlib.pyplot as plt


# for latex font
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

# data, model
datasets = ["asia", "asia", "asia", "asia"]
model = "cnb"

plot_titles = [r"Asia", r"Sachs", r"Alarm", r"Hepar II"]

fig, ax = plt.subplots(1, 4, figsize=(8, 3))
# fig, ax = plt.subplots()
plt.tight_layout(pad=1)

for i in range(4):
    data = datasets[i]
    # load data
    runtime = pd.read_csv(f"results/discrete/{data}/metadata_{data}_{model}.csv")
    runtime = runtime[["runtime sage", "runtime cg", "runtime cg est"]].to_numpy()

    rt = []
    rt.append(runtime[0][0])
    rt.append(runtime[0][1])
    rt.append(runtime[0][2])

    # runtime g learning
    if data == "asia":
        g_rt = [0, 0, 0.067]
    elif data == "sachs":
        g_rt = [0, 0, 0.098]
    elif data == "alarm":
        g_rt = [0, 0, 0.76]
    elif data == "hepar":
        g_rt = [0, 0, 1.833]

    labels = [r"SAGE", r"SAGE$_{cg}$", r"SAGE$_{cg}^{*}$"]

    ax[i].bar(labels, rt, width=0.4, label='SAGE', color="tab:grey")
    ax[i].bar(labels, g_rt, width=0.4, bottom=rt,
              label='TABU', color="orange")

    ax[i].set_ylabel('Runtime in s')
    ax[i].set_title(plot_titles[i])
    if i == 3:
        ax[i].legend(loc='upper right')
    if i > 0:
        ax[i].set_ylabel('')
    for tick in ax[i].get_xticklabels():
        tick.set_rotation(60)

fig.subplots_adjust(bottom=0.28)

plt.savefig(f"results/plots/runtime_sage_{model}.png", dpi=400, bbox_inches='tight')
