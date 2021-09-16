"""File creates graphs and adjacency matrices using the networkx package and dumps them using pickle
    input:
        adjacency matrix in csv format (e.g. from structure learning in R)
"""
import networkx as nx
import pandas as pd
import pickle
import sys
import os
import inspect


current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


from functions import create_folder

# create folder to store models
create_folder(".results_py/")

# specify names of graphs to loop through
names = ["asia_s", "asia_m", "asia_l", "asia_xl",
         "sachs_s", "sachs_m", "sachs_l", "sachs_xl",
         "alarm_s", "alarm_m", "alarm_l", "alarm_xl",
         "hepar_s", "hepar_m", "hepar_l", "hepar_xl",
         "dag_s_1000_obs", "dag_s_10000_obs", "dag_s_100000_obs", "dag_s_1000000_obs",
         "dag_m_1000_obs", "dag_m_10000_obs", "dag_m_100000_obs", "dag_m_1000000_obs",
         "dag_l_1000_obs", "dag_l_10000_obs", "dag_l_100000_obs", "dag_l_1000000_obs"]

names_true = ["asia", "alarm", "sachs", "hepar", "dag_s", "dag_m", "dag_l"]

# specify methods used during structure learning
methods = ["hc", "tabu", "mmhc", "iiamb", "h2pc", "gs"]

# estimated or true adjacency matrices
estimated = False


if estimated:
    # loop through method in methods
    for method in methods:
        # loop through graphs
        for i in names:
            # load adjacency matrix as csv file
            df = pd.read_csv(
                f"bnlearn/results/{method}/est_amat/{i}.csv"
            )
            mapping_rf = {"FALSE": 0, "TRUE": 1}
            col_names = df.columns.tolist()
            for j in col_names:
                df[j] = df.replace({j: mapping_rf})[j]
            index = df.index
            # modify adjacency matrix for use in networkx package
            var_names = df.columns.to_list()
            df = df.set_axis(var_names, axis=0)
            # store modified adjacency matrix
            create_folder(f"results_py/{method}/est_amat/")
            pickle.dump(df, open(f"results_py/{method}/est_amat/{i}.p", "wb"))
            g = nx.DiGraph(df)
            create_folder(f"results_py/{method}/graphs/")
            filename = f"results_py/{method}/graphs/{i}/.p"
            pickle.dump(g, open(filename, "wb"))
else:
    for i in names_true:
        df = pd.read_csv(f"bnlearn/true_amat/{i}.csv")
        mapping_rf = {"FALSE": 0, "TRUE": 1}
        col_names = df.columns.tolist()
        for j in col_names:
            df[j] = df.replace({j: mapping_rf})[j]
        var_names = df.columns.to_list()
        df = df.set_axis(var_names, axis=0)
        create_folder(f"results_py/true_amat/")
        pickle.dump(df, open(f"results_py/true_amat/{i}.p", "wb"))
        g = nx.DiGraph(df)
        create_folder(f"results_py/true_graphs/")
        filename = f"results_py/true_graphs/{i}.p"
        pickle.dump(g, open(filename, "wb"))
