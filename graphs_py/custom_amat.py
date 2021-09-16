"""Template to create custom adjacency matrix and graph
"""
import networkx as nx
import pandas as pds
import pickle
import matplotlib.pyplot as plt

data = [[0, 0, 0, 1, 1], [0, 0, 1, 0, 1], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0]]
var_names = ["m1", "m2", "m3", "m4", "y"]
df = pd.DataFrame(data, columns=var_names)
df = df.set_axis(var_names, axis=0)
pickle.dump(df, open(f"results_py/true_amat_py/cma.p", "wb"))
g = nx.DiGraph(df)
filename = f"results_py/true_graphs_py/cma.p"
pickle.dump(g, open(filename, "wb"))
nx.draw(g)
plt.show()
