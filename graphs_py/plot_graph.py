import pickle
import networkx as nx
import matplotlib.pyplot as plt

path = "results_py/true_amat/dag_s.p"
amat = pickle.load(open(path, "rb"))

g = nx.DiGraph(amat)
nx.draw(g)
plt.show()

