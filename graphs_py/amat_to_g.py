"""File creates graphs and adjacency matrices using the networkx package and dumps them using pickle
    input:
        adjacency matrix in csv format (e.g. from structure learning in R)
"""
import networkx as nx
import pandas as pd
import pickle


# specify names of graphs to loop through
names = ["asia", "alarm", "sachs", "pathfinder", "cont_small", "cont_medium", "cont_large"]
# specify methods used during structure learning
methods = ["hc", "tabu", "mmhc", "notears"]
# estimated or true adjacency matrices
estimated = True


if estimated:
    # loop through method in methods
    for method in methods:
        # loop through graphs
        for i in names:
            # loop through sample sizes
            for j in ["s", "m", "l", "xl"]:
                # load adjacency matrix as csv file
                df = pd.read_csv(
                    f"bnlearn/results/{method}/est_amat/{i}_{j}.csv"
                )
                index = df.index
                print(index)
                print(df.columns)
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
        df = pd.read_csv(f"bnlearn/true_amat/{i}.csv")
        var_names = df.columns.to_list()
        df = df.set_axis(var_names, axis=0)
        pickle.dump(df, open(f"results_py/true_amat_py/{i}.p", "wb"))
        g = nx.DiGraph(df)
        filename = f"results_py/true_graphs_py/{i}.p"
        pickle.dump(g, open(filename, "wb"))
