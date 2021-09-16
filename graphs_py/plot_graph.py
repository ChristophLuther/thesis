import pickle
import networkx as nx
import matplotlib.pyplot as plt

path = "results_py/true_amat/dag_s.p"
amat = pickle.load(open(path, "rb"))

g = nx.DiGraph(amat)

nx.draw(g, with_labels=True, font_weight="bold")
plt.show()
# plt.savefig("results_py/tabu/graphs/pngs/asia/asia_l.png")
