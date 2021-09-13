"""Visualization of graph comparison"""

# test_branch push and merge
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("results_py/graph_evaluation.csv")

x = ["1k", "10k", "100k", "1000k"]

y1 = df[df['csl method'] == "hc"]  # hc
y2 = df[df['csl method'] == "tabu"]   # tabu

y1_asia = y1[y1['graph'] == "asia"]["F1"]
y2_asia = y2[y2['graph'] == "asia"]["F1"]

y1_sachs = y1[y1['graph'] == "sachs"]["F1"]
y2_sachs = y2[y2['graph'] == "sachs"]["F1"]

y1_survey = y1[y1['graph'] == "survey"]["F1"]
y2_survey = y2[y2['graph'] == "survey"]["F1"]

# plt.figure(figsize=(8, 5))
# mark = ["1k","10k","100k","1000k"]
# plt.scatter(x, y1, color='red')
# plt.scatter(x, y2, color='blue')
# plt.plot(x, y1, color='red', linestyle='-', markevery=mark)
# plt.plot(x, y2, color='blue', linestyle='--', markevery=mark)
# plt.show()

mark = ["1k", "10k", "100k", "1000k"]
fig, axes = plt.subplots(1, 3, figsize=(9, 3))
fig.suptitle("F1 Score - D-Separation Inference", fontsize=12)

axes[0].scatter(x, y1_asia, color='red')
axes[0].scatter(x, y2_asia, color='blue')
axes[0].plot(x, y1_asia, color='red', linestyle='-', markevery=mark)
axes[0].plot(x, y2_asia, color='blue', linestyle='--', markevery=mark)

axes[1].scatter(x, y1_sachs, color='red')
axes[1].scatter(x, y2_sachs, color='blue')
axes[1].plot(x, y1_sachs, color='red', linestyle='-', markevery=mark)
axes[1].plot(x, y2_sachs, color='blue', linestyle='--', markevery=mark)

axes[2].scatter(x, y1_survey, color='red')
axes[2].scatter(x, y2_survey, color='blue')
axes[2].plot(x, y1_survey, color='red', linestyle='-', markevery=mark)
axes[2].plot(x, y2_survey, color='blue', linestyle='--', markevery=mark)
plt.savefig("visualization/dseps/test.png")
plt.show()
plt.clf()


# plot number of inferred d-seps / number of true d-seps
