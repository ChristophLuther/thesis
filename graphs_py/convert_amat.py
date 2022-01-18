"""File creates graphs and adjacency matrices using the networkx package and stores them
    input:
        adjacency matrix in csv format (e.g. from structure learning in R)
"""
import pandas as pd
import sys
import os
import inspect
import argparse

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


from utils import create_folder


parser = argparse.ArgumentParser(
    description="Convert adjacency matrix to format for nx")

parser.add_argument(
    "-a",
    "--amat",
    type=str,
    default="estimated",
    help="Is amat estimated? Default is estimated: 'estimated' or 'no'")

parser.add_argument(
    "-d",
    "--data",
    type=str,
    default="discrete",
    help="Discrete or Continuous data? 'continuous' or 'discrete'",
)

args = parser.parse_args()

# create folder to store models
create_folder("results_py/")

# specify names of graphs to loop through
if args.data == "discrete":
    #names = ["sachs_1000_obs", "sachs_10000_obs", "sachs_1e+05_obs", "sachs_1e+06_obs", "sachs_2e+06_obs",
    #         "asia_1000_obs", "asia_10000_obs", "asia_1e+05_obs", "asia_1e+06_obs", "asia_2e+06_obs",
    #         "alarm_1000_obs", "alarm_10000_obs", "alarm_1e+05_obs", "alarm_1e+06_obs", "alarm_2e+06_obs",
    #        "hepar_1000_obs", "hepar_10000_obs", "hepar_1e+05_obs", "hepar_1e+06_obs", "hepar_2e+06_obs"]

    names = ["sachs_10_obs", "sachs_100_obs", "sachs_1000_obs", "sachs_10000_obs", "sachs_20000_obs",
             "asia_10_obs", "asia_100_obs", "asia_1000_obs", "asia_10000_obs", "asia_20000_obs",
             "alarm_10_obs", "alarm_100_obs", "alarm_1000_obs", "alarm_10000_obs", "alarm_20000_obs",
             "hepar_10_obs", "hepar_100_obs", "hepar_1000_obs", "hepar_10000_obs", "hepar_20000_obs"]

    names_true = ["sachs", "asia", "alarm", "hepar"]
    methods = ["hc", "tabu", "mmhc", "h2pc"]

else:
    #names = ["dag_s_1000_obs", "dag_s_10000_obs", "dag_s_100000_obs", "dag_s_1000000_obs", "dag_s_2000000_obs",
    #         "dag_sm_1000_obs", "dag_sm_10000_obs", "dag_sm_100000_obs", "dag_sm_1000000_obs", "dag_sm_2000000_obs",
    #        "dag_m_1000_obs", "dag_m_10000_obs", "dag_m_100000_obs", "dag_m_1000000_obs", "dag_m_2000000_obs",
    #        "dag_l_1000_obs", "dag_l_10000_obs", "dag_l_100000_obs", "dag_l_1000000_obs", "dag_l_2000000_obs"]

    names = ["dag_s_10_obs", "dag_s_100_obs", "dag_s_1000_obs", "dag_s_10000_obs", "dag_s_20000_obs",
             "dag_sm_10_obs", "dag_sm_100_obs", "dag_sm_1000_obs", "dag_sm_10000_obs", "dag_sm_20000_obs",
             "dag_m_10_obs", "dag_m_100_obs", "dag_m_1000_obs", "dag_m_10000_obs", "dag_m_20000_obs",
             "dag_l_10_obs", "dag_l_100_obs", "dag_l_1000_obs", "dag_l_10000_obs", "dag_l_20000_obs"]

    names_true = ["dag_s", "dag_sm", "dag_m", "dag_l"]
    methods = ["hc", "tabu"]


def convert_amat(arg):
    if arg.amat == "estimated":
        # loop through method in methods
        for method in methods:
            create_folder(f"results_py/{method}")
            # loop through graphs
            for i in names:
                # load adjacency matrix as csv file
                df = pd.read_csv(
                    f"bnlearn/results/{method}/{i}.csv")

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
                df.to_csv(f"results_py/{method}/{i}.csv", index=True)

    else:
        for i in names_true:
            df = pd.read_csv(f"data/true_amat/{i}.csv")

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
            df.to_csv(f"results_py/true_amat/{i}.csv", index=True)


if __name__ == "__main__":
    convert_amat(args)
