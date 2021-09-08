"""Evaluate structure learning performance measured by ability to learn d-separations"""
import pickle
from comparison import GraphComparison
import pandas as pd

# in case I want to loop through graph names
names = ["alarm", "asia", "pathfinder", "sachs", "cont_small", "cont_medium", "cont_large"]

targets_sink = {"alarm": "TBD", "asia": "dysp", "pathfinder": "TBD", "sachs": "Akt",
                "cont_small": "y", "cont_medium": "y", "cont_large": "y"}

targets_mid = {"alarm": "CATECHOL", "asia": "dysp", "pathfinder": "TBD", "sachs": "Akt",
               "cont_small": "y", "cont_medium": "y", "cont_large": "y"}    # TODO change

methods = ["hc", "tabu", "mmhc"]

sizes = ["s", "m", "l", "xl"]

graph_evaluation = pd.read_csv("results_py/graph_evaluation.csv")

for method in methods:
    for graph in names:
        for size in sizes:
            # exact graph
            path_true = f"true_graphs_py/{graph}.p"
            # path to estimated graph
            path_est = f"results_py/{method}/graphs/{graph}/{graph}_{size}.p"

            # load true graph
            g_true = pickle.load(open(path_true, "rb"))
            # load estimated graph
            g_est = pickle.load(open(path_est, "rb"))

            # number of nodes
            d = len(g_true.nodes)
            # potential d-separations w.r.t. y
            potential_dseps = (d - 1) * (2 ** (d - 2))

            target_node = targets_sink["graph"]

            # comparison instance
            if potential_dseps < 100000:
                survey_comp = GraphComparison(g_true, g_est, target_node)
                mc = "n/a"
            else:
                mc = 100000
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
            precision = TP / (TP+FP)
            recall = TP_rate
            F1 = (2 * precision * recall) / (precision + recall)

            content = [graph, target_node, d, potential_dseps, size, method, mc, true_total, false_total, dsep_share,
                       TP, TN, FP, FN, TP_rate, TN_rate, FP_rate, FN_rate, precision, recall, F1]
            # fill evaluation table with current run
            graph_evaluation.loc[len(graph_evaluation)] = content

graph_evaluation.to_csv(
            "results_py/graph_evaluation.csv", index=False
        )
