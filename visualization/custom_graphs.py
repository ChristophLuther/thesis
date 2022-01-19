'''Example on how to create custom graph using Networkx (nx) package'''

import networkx as nx
import matplotlib.pyplot as plt


g1 = nx.DiGraph()
# nodes
g1.add_node(1, label='$X_1$', shape='circle')
g1.add_node(2, label='$X_2$', shape='circle')
g1.add_node(3, label='$X_3$', shape='circle')
g1.add_node(3, label='$X_4$', shape='circle')
# edges
g1.add_edge(1, 2)
g1.add_edge(3, 2)
g1.add_edge(3, 4, color='red')

g2 = nx.DiGraph()
# nodes
g2.add_node(1, label='$X_1$', shape='circle')
g2.add_node(2, label='$X_2$', shape='circle')
g2.add_node(3, label='$X_3$', shape='circle')
g2.add_node(3, label='$X_4$', shape='circle')
# edges
g2.add_edge(1, 2)
g2.add_edge(3, 2)
g2.add_edge(4, 3, color='blue')


nx.draw(g1)
savepath = "~/exemplary_graph"
plt.savefig(f"{savepath}.png")
