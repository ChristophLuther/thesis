"""Evaluate structure learning performance measured by ability to learn d-separations"""
import pickle
from comparison import GraphComparison
import pandas as pd
import argparse
import sys
import os
import inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


parser = argparse.ArgumentParser(
    description="convert adjacency matrix to format for nx")

parser.add_argument(
    "-m",
    "--method",
    type=str,
    default="all",
    help="What methods were used?",
)

parser.add_argument(
    "-d",
    "--data",
    type=str,
    default="all",
    help="What dataset?",
)

parser.add_argument(
    "-t",
    "--target",
    type=str,
    default="y",
    help="What target?",
)

parser.add_argument(
    "-n",
    "--sample_size",
    type=int,
    default=None,
    help="What sample size?",
)

parser.add_argument(
    "-m",
    "--mc",
    type=int,
    default=100000,
    help="What mc?",
)

# if n is None : 1000, 10000, 100000, 1000000

args = parser.parse_args()


def compare_graphs(arg):
    # read graph evaluation csv or create if not existent
    try:
        graph_evaluation = pd.read_csv("results_py/graph_evaluation.csv")
    except:
        col_names = ["graph", "target_node", "d", "potential_dseps", "method", "mc",
                     "true_total", "false_total", "dsep_share", "TP", "TN", "FP", "FN", "TP_rate",
                     "TN_rate", "FP_rate", "FN_rate", "precision", "recall", "F1"]
        graph_evaluation = pd.DataFrame(columns=col_names)

    if arg.method == "all":
        methods = ["hc", "tabu", "mmhc", "iiamb", "gs", "h2pc"]
    else:
        methods = [arg.method]

    if arg.data == "all":
        names = ["alarm_s", "asia_s", "hepar_s", "sachs_s",
                 "alarm_m", "asia_m", "hepar_m", "sachs_m",
                 "alarm_l", "asia_l", "hepar_l", "sachs_l",
                 "alarm_xl", "asia_xl", "hepar_xl", "sachs_xl"]
    else:
        names = [arg.data]

    if arg.target == "y":
        if arg.data == "all":
            targets_mid = {"alarm_s": "CATECHOL", "asia_s": "dysp", "hepar_s": "Cirrhosis", "sachs_s": "Erk",
                           "alarm_m": "CATECHOL", "asia_m": "dysp", "hepar_m": "Cirrhosis", "sachs_m": "Erk",
                           "alarm_l": "CATECHOL", "asia_l": "dysp", "hepar_l": "Cirrhosis", "sachs_l": "Erk",
                           "alarm_xl": "CATECHOL", "asia_xl": "dysp", "hepar_xl": "Cirrhosis", "sachs_xl": "Erk"}
        else:
            targets_mid = {arg.data: "y"}
    else:
        targets_mid = {arg.data: arg.target}

    if arg.sample_size is None:
        sample

    for alg in methods:
        for graph in names:
            # exact graph
            path_true = f"results_py/true_graphs/{graph}.p"
            # path to estimated graph
            path_est = f"results_py/{alg}/graphs/{graph}.p"
            # load true graph
            g_true = pickle.load(open(path_true, "rb"))
            # load estimated graph
            g_est = pickle.load(open(path_est, "rb"))
            # number of nodes
            d = len(g_true.nodes)
            # potential d-separations w.r.t. y
            potential_dseps = (d - 1) * (2 ** (d - 2))
            target_node = targets_mid[graph]
            # comparison instance
            if potential_dseps < arg.mc:
                survey_comp = GraphComparison(g_true, g_est, target_node)
                mc = "n/a"
            else:
                mc = arg.mc
                survey_comp = GraphComparison(g_true, g_est, target_node, mc=mc, rand_state=42)
            # true total and false total are ground truth
            TP, TN, FP, FN, true_total, false_total = survey_comp.exact()
            # share of dseps (just make a note, if d-separations were approximated via mc)
            dsep_share = true_total / (true_total + false_total)
            # and don't forget to mention the number of mc
            # graph specific table
            # then TP-, TN-, FP-, and FN-rate as above
            TP_rate = TP / true_total
            FN_rate = FN / true_total
            TN_rate = TN / false_total
            FP_rate = FP / false_total
            # F1 score
            precision = TP / (TP + FP)
            recall = TP_rate
            F1 = (2 * precision * recall) / (precision + recall)
            content = [graph, target_node, d, potential_dseps, alg, mc, true_total, false_total,
                       dsep_share,
                       TP, TN, FP, FN, TP_rate, TN_rate, FP_rate, FN_rate, precision, recall, F1]
            # fill evaluation table with current run
            graph_evaluation.loc[len(graph_evaluation)] = content

    graph_evaluation.to_csv(
        "results_py/graph_evaluation.csv", index=False
    )


if __name__ == "__main__":
    compare_graphs(args)
