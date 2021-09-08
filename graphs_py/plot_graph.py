import pickle
import networkx as nx
import matplotlib.pyplot as plt

path = "results_py/tabu/graphs/asia/asia_l.p"
g = pickle.load(open(path, "rb"))
nx.draw(g, with_labels=True, font_weight="bold")
plt.savefig("results_py/tabu/graphs/pngs/asia/asia_l.png")
