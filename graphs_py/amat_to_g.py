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
import argparse

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


from functions import create_folder


# TODO make names, names_true and methods arguments for parser
parser = argparse.ArgumentParser(
    description="convert adjacency matrix to format for nx")

parser.add_argument(
    "-e",
    "--amat",
    type=bool,
    default=True,
    help="Is amat estimated? Default is True, i.e. amat is estimated",
)

args = parser.parse_args()

# create folder to store models
create_folder("results_py/")

# specify names of graphs to loop through
names = ["dag_s_1000_obs", "dag_s_10000_obs", "dag_s_1e+05_obs", "dag_s_1e+06_obs",
         "dag_m_1000_obs", "dag_m_10000_obs", "dag_m_1e+05_obs", "dag_m_1e+06_obs",
         "dag_l_1000_obs", "dag_l_10000_obs", "dag_l_1e+05_obs", "dag_l_1e+06_obs"]

names_true = ["dag_s", "dag_m", "dag_l"]

# specify methods used during structure learning
methods = ["hc", "tabu"]    # TODO  make method an input argument or adapt methods ("h2pc", "mmhc")


def convert_amat(arg):
    if arg.amat:
        # loop through method in methods
        for method in methods:
            create_folder(f"results_py/{method}")
            # loop through graphs
            for i in names:
                # load adjacency matrix as csv file
                df = pd.read_csv(
                    f"bnlearn/results/{method}/est_amat/{i}.csv")

                col_names_int = []

                for k in range(len(df.columns)):
                    col_names_int.append(k+1)

                df.columns = col_names_int

                mapping_rf = {False: 0, True: 1}
                col_names = df.columns.tolist()
                for j in col_names:
                    df[j] = df.replace({j: mapping_rf})[j]

                # modify adjacency matrix for use in networkx package
                var_names = df.columns.to_list()
                df = df.set_axis(var_names, axis=0)
                # store modified adjacency matrix
                create_folder(f"results_py/{method}/est_amat/")
                pickle.dump(df, open(f"results_py/{method}/est_amat/{i}.p", "wb"))
                g = nx.DiGraph(df)
                create_folder(f"results_py/{method}/graphs/")
                filename = f"results_py/{method}/graphs/{i}.p"
                pickle.dump(g, open(filename, "wb"))
    else:
        for i in names_true:
            df = pd.read_csv(f"bnlearn/true_amat/{i}.csv")

            col_names_int = []

            for k in range(len(df.columns)):
                col_names_int.append(k + 1)

            df.columns = col_names_int

            mapping_rf = {False: 0, True: 1}
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


if __name__ == "__main__":
    convert_amat(args)
