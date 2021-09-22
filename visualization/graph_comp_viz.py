"""Visualization of graph comparison"""
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
import inspect


current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


from functions import create_folder

create_folder(".dseps/")

df = pd.read_csv("visualization/graph_evaluation.csv")

x = ["1k", "10k", "100k", "1000k"]

y1 = df[df['method'] == "hc"]  # hc
y2 = df[df['method'] == "tabu"]   # tabu
y3 = df[df['method'] == "mmhc"]   # mmhc
y4 = df[df['method'] == "h2pc"]   # h2pc

y1_asia = y1[y1['d'] == 8]["F1"]
y2_asia = y2[y2['d'] == 8]["F1"]
y3_asia = y3[y3['d'] == 8]["F1"]
y4_asia = y4[y4['d'] == 8]["F1"]


y1_sachs = y1[y1['d'] == 11]["F1"]
y2_sachs = y2[y2['d'] == 11]["F1"]
y3_sachs = y3[y3['d'] == 11]["F1"]
y4_sachs = y4[y4['d'] == 11]["F1"]

y1_hepar = y1[y1['d'] == 70]["F1"]
y2_hepar = y2[y2['d'] == 70]["F1"]
y3_hepar = y3[y3['d'] == 70]["F1"]
y4_hepar = y4[y4['d'] == 70]["F1"]

y1_alarm = y1[y1['d'] == 37]["F1"]
y2_alarm = y2[y2['d'] == 37]["F1"]
y3_alarm = y3[y3['d'] == 37]["F1"]
y4_alarm = y4[y4['d'] == 37]["F1"]

# plt.figure(figsize=(8, 5))
# mark = ["1k","10k","100k","1000k"]
# plt.scatter(x, y1, color='red')
# plt.scatter(x, y2, color='blue')
# plt.plot(x, y1, color='red', linestyle='-', markevery=mark)
# plt.plot(x, y2, color='blue', linestyle='--', markevery=mark)
# plt.show()

mark = ["1k", "10k", "100k", "1000k"]
fig, axes = plt.subplots(2, 2, figsize=(9, 3))
fig.suptitle("F1 Score - D-Separation Inference", fontsize=12)

axes[0, 0].scatter(x, y1_asia, color='c')
axes[0, 0].scatter(x, y2_asia, color='y')
axes[0, 0].scatter(x, y3_asia, color='m')
axes[0, 0].scatter(x, y4_asia, color='g')
l1 = axes[0, 0].plot(x, y1_asia, color='c', linestyle='-', markevery=mark)
l2 = axes[0, 0].plot(x, y2_asia, color='y', linestyle=':', markevery=mark)
l3 = axes[0, 0].plot(x, y3_asia, color='m', linestyle='--', markevery=mark)
l4 = axes[0, 0].plot(x, y4_asia, color='g', linestyle='-.', markevery=mark)

axes[0, 1].scatter(x, y1_sachs, color='c')
axes[0, 1].scatter(x, y2_sachs, color='y')
axes[0, 1].scatter(x, y3_sachs, color='m')
axes[0, 1].scatter(x, y4_sachs, color='g')
axes[0, 1].plot(x, y1_sachs, color='c', linestyle='-', markevery=mark)
axes[0, 1].plot(x, y2_sachs, color='y', linestyle=':', markevery=mark)
axes[0, 1].plot(x, y3_sachs, color='m', linestyle='--', markevery=mark)
axes[0, 1].plot(x, y4_sachs, color='g', linestyle='-.', markevery=mark)

axes[1, 0].scatter(x, y1_alarm, color='c')
axes[1, 0].scatter(x, y2_alarm, color='y')
axes[1, 0].scatter(x, y3_alarm, color='m')
axes[1, 0].scatter(x, y4_alarm, color='g')
axes[1, 0].plot(x, y1_alarm, color='c', linestyle='-', markevery=mark)
axes[1, 0].plot(x, y2_alarm, color='y', linestyle=':', markevery=mark)
axes[1, 0].plot(x, y3_alarm, color='m', linestyle='--', markevery=mark)
axes[1, 0].plot(x, y4_alarm, color='g', linestyle='-.', markevery=mark)

axes[1, 1].scatter(x, y1_hepar, color='c')
axes[1, 1].scatter(x, y2_hepar, color='y')
axes[1, 1].scatter(x, y3_hepar, color='m')
axes[1, 1].scatter(x, y4_hepar, color='g')
axes[1, 1].plot(x, y1_hepar, color='c', linestyle='-', markevery=mark)
axes[1, 1].plot(x, y2_hepar, color='y', linestyle=':', markevery=mark)
axes[1, 1].plot(x, y3_hepar, color='m', linestyle='--', markevery=mark)
axes[1, 1].plot(x, y4_hepar, color='g', linestyle='-.', markevery=mark)

line_labels = ["hc", "tabu", "mmhc", "h2pc"]
fig.legend([l1, l2, l3, l4],     # The line objects
           labels=line_labels,   # The labels for each line
           loc="center right",   # Position of legend
           borderaxespad=0.1,    # Small spacing around legend box
           title="Legend Title"  # Title for the legend
           )

# plt.savefig("visualization/dseps/test.png")
plt.show()
plt.clf()


# plot number of inferred d-seps / number of true d-seps
