"""File to evaluate estimated graphs wrt inferred d-separations by comparison to
    ground truth graph using GraphComparison class from comparison.py used in
    Causal Structure Learning for SAGE Estimation

    """
import networkx as nx
import pandas as pd
import sys
import os
import inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from graphs_py.utils import exact, approx

# file for comparison
try:
    graph_evaluation = pd.read_csv("results_py/graph_evaluation.csv")
except:
    col_names = ["Graph", "Target", "Method", "MC",
                 "True total", "False total", "D-sep share", "TP", "TN", "FP", "FN", "TP rate",
                 "TN rate", "FP rate", "FN rate", "Precision", "Recall", "F1"]
    graph_evaluation = pd.DataFrame(columns=col_names)

# to access the target nodes in graph loop
targets = {"alarm": "PULMEMBOLUS", "asia": "dysp", "hepar": "RHepatitis", "sachs": "Erk",
           "dag_s": "1",  "dag_sm": "1",  "dag_m": "1",  "dag_l": "1"}


# compare graphs with less than 1M d-separations by evaluating exact inference
'''
for graph in ["asia", "sachs", "alarm", "hepar"]:
    # ground truth graph
    true_amat = pd.read_csv(f"results_py/true_amat/{graph}.csv", index_col=0)
    g_true = nx.DiGraph(true_amat)
    for method in ["hc", "tabu", "mmhc", "h2pc"]:
        for n in ["10", "100", "1000", "10000", "20000"]:
            est_amat = pd.read_csv(f"results_py/{method}/{graph}_{n}_obs.csv", index_col=0)
            g_est = nx.DiGraph(est_amat)
            if graph in ["asia", "sachs"]:
                tp, tn, fp, fn, d_separated_total, d_connected_total = exact(g_true, g_est, targets[f"{graph}"])
                mc = "n/a"
            elif graph in ["alarm", "hepar"]:
                mc = 1000
                tp, tn, fp, fn, d_separated_total, d_connected_total = approx(g_true, g_est, targets[f"{graph}"],
                                                                              mc=mc, rand_state=42)
            else:
                print("graph is not defined properly")
                break

            dsep_share = d_separated_total / (d_separated_total + d_connected_total)
            if d_separated_total == 0:
                TP_rate = 0
                FN_rate = 0
            else:
                TP_rate = tp / d_separated_total
                FN_rate = fn / d_separated_total
            if d_connected_total == 0:
                TN_rate = 0
                FP_rate = 0
            else:
                TN_rate = tn / d_connected_total
                FP_rate = fp / d_connected_total
            # F1 score
            precision = tp / (tp + fp)
            recall = TP_rate
            F1 = (2 * precision * recall) / (precision + recall)
            content = [f"{graph}_{n}_obs", targets[f"{graph}"], method, mc, d_separated_total, d_connected_total,
                       dsep_share, tp, tn, fp, fn, TP_rate, TN_rate, FP_rate, FN_rate, precision, recall, F1]
            graph_evaluation.loc[len(graph_evaluation)] = content
'''
for graph in ["dag_s", "dag_sm", "dag_m", "dag_l"]:
    # ground truth graph
    true_amat = pd.read_csv(f"results_py/true_amat/{graph}.csv", index_col=0)
    true_amat.index = true_amat.index.map(str)
    g_true = nx.DiGraph(true_amat)
    for method in ["hc", "tabu"]:
        for n in ["10", "100", "1000", "10000", "20000"]:
            est_amat = pd.read_csv(f"results_py/{method}/{graph}_{n}_obs.csv", index_col=0)
            est_amat.index = est_amat.index.map(str)
            g_est = nx.DiGraph(est_amat)
            if graph in ["dag_s"]:
                tp, tn, fp, fn, d_separated_total, d_connected_total = exact(g_true, g_est, targets[f"{graph}"])
                mc = "n/a"
            elif graph in ["dag_sm", "dag_m", "dag_l"]:
                mc = 1000
                tp, tn, fp, fn, d_separated_total, d_connected_total = approx(g_true, g_est, targets[f"{graph}"],
                                                                              mc=mc, rand_state=42)
            else:
                print("graph is not defined properly")
                break
            dsep_share = d_separated_total / (d_separated_total + d_connected_total)
            if d_separated_total == 0:
                TP_rate = 0
                FN_rate = 0
            else:
                TP_rate = tp / d_separated_total
                FN_rate = fn / d_separated_total
            if d_connected_total == 0:
                TN_rate = 0
                FP_rate = 0
            else:
                TN_rate = tn / d_connected_total
                FP_rate = fp / d_connected_total
            # F1 score
            try:
                precision = tp / (tp + fp)
            except:
                precision = 0
            recall = TP_rate
            try:
                F1 = (2 * precision * recall) / (precision + recall)
            except:
                F1 = 0
            content = [f"{graph}_{n}_obs", targets[f"{graph}"], method, mc, d_separated_total, d_connected_total,
                       dsep_share, tp, tn, fp, fn, TP_rate, TN_rate, FP_rate, FN_rate, precision, recall, F1]
            graph_evaluation.loc[len(graph_evaluation)] = content

graph_evaluation.to_csv("results_py/graph_evaluation.csv", index=False)
