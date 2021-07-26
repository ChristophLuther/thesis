import networkx as nx
import pandas as pd
import pickle
# import matplotlib.pyplot as plt


# specify names of graphs to loop through
names = [
    "alarm",
    "asia",
    "child",
    "hail",
    "hepar",
    "insurance",
    "mildew",
    "sachs",
    "survey",
]

# specify method used during structure learning
method = "hc"
# estimated or true adjacency matrices
estimated = True


if estimated is True:
    # loop through graphs
    for i in names:
        # loop through sample sizes
        for j in ["s", "m", "l", "xl"]:
            # load adjacency matrix as csv file
            df = pd.read_csv(f"bnlearnR/results_py/{method}/est_amat/{i}/{i}_{j}.csv")
            # modify adjacency matrix for use in networkx package
            var_names = df.columns.to_list()
            df = df.set_axis(var_names, axis=0)
            # store modified adjacency matrix
            pickle.dump(df, open(f"results_py/{method}/est_amat/{i}/{i}_{j}.p", "wb"))
            g = nx.DiGraph(df)
            filename = f"results_py/{method}/graphs/{i}/{i}_{j}.p"
            pickle.dump(g, open(filename, "wb"))
else:
    for i in names:
        df = pd.read_csv(f"bnlearnR/true_amat/{i}.csv")
        var_names = df.columns.to_list()
        df = df.set_axis(var_names, axis=0)
        pickle.dump(df, open(f"true_amat_py/{i}.p", "wb"))
        g = nx.DiGraph(df)
        filename = f"true_graphs_py/{i}.p"
        pickle.dump(g, open(filename, "wb"))

# nx.draw(g, with_labels=True, font_weight="bold")
# plt.show()
