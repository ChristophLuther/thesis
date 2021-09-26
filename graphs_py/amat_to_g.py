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
    "-a",
    "--amat",
    type=str,
    default="estimated",
    help="Is amat estimated? Default is True, i.e. amat is estimated")

parser.add_argument(
    "-d",
    "--data",
    type=str,
    default="discrete",
    help="Discrete or Continuous data?",
)

args = parser.parse_args()
print(args.amat)
print(args.data)
# create folder to store models
create_folder("results_py/")

# specify names of graphs to loop through
if args.data == "discrete":
    names = ["sachs_1000_obs", "sachs_10000_obs", "sachs_1e+05_obs", "sachs_1e+06_obs", "sachs_2e+06_obs",
             "asia_1000_obs", "asia_10000_obs", "asia_1e+05_obs", "asia_1e+06_obs", "asia_2e+06_obs",
             "alarm_1000_obs", "alarm_10000_obs", "alarm_1e+05_obs", "alarm_1e+06_obs", "alarm_2e+06_obs",
             "hepar_1000_obs", "hepar_10000_obs", "hepar_1e+05_obs", "hepar_1e+06_obs", "hepar_2e+06_obs"]

    names_true = ["sachs", "asia", "alarm", "hepar"]
    methods = ["hc", "tabu", "mmhc", "h2pc"]

else:
    names = ["dag_s_1000_obs", "dag_s_10000_obs", "dag_s_1e+05_obs", "dag_s_1e+06_obs", "dag_s_2e+06_obs",
             "dag_m_1000_obs", "dag_m_10000_obs", "dag_m_1e+05_obs", "dag_m_1e+06_obs", "dag_m_2e+06_obs",
             "dag_l_1000_obs", "dag_l_10000_obs", "dag_l_1e+05_obs", "dag_l_1e+06_obs", "dag_l_2e+06_obs"]

    names_true = ["dag_s", "dag_m", "dag_l"]
    methods = ["hc", "tabu", "mmhc"]


def convert_amat(arg):
    if arg.amat == "estimated":
        # loop through method in methods
        for method in methods:
            create_folder(f"results_py/{method}")
            # loop through graphs
            for i in names:
                # load adjacency matrix as csv file
                df = pd.read_csv(
                    f"bnlearn/results/{method}/est_amat/{i}.csv")

                if arg.data == "continuous":
                    col_names_str = []
                    for k in range(len(df.columns)):
                        col_names_str.append(str(k+1))
                    df.columns = col_names_str

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

            if arg.data == "continuous":
                col_names_str = []
                for k in range(len(df.columns)):
                    col_names_str.append(str(k + 1))
                df.columns = col_names_str

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
