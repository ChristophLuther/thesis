"""Single file to compare graphs"""
import pickle
import pandas as pd
import random
import numpy as np
import scipy.special as sp
import networkx as nx
import sys
import os
import inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from functions import d_separation



# file for comparison
try:
    graph_evaluation = pd.read_csv("results_py/graph_evaluation.csv")
except:
    col_names = ["graph", "target_node", "d", "method", "mc",
                 "true_total", "false_total", "dsep_share", "TP", "TN", "FP", "FN", "TP_rate",
                 "TN_rate", "FP_rate", "FN_rate", "precision", "recall", "F1"]
    graph_evaluation = pd.DataFrame(columns=col_names)


# to loop through graphs
graphs = ["dag_s"]
graphs_mc = ["dag_m", "dag_s"]
random.seed(42)
np.random.seed(42)
rng = np.random.default_rng(seed=42)

# to loop through sizes
sizes = ["1000", "10000", "1e+05", "1e+06"]

# to loop through graph learning algorithms
algs = ["hc", "tabu"]

for graph in graphs:
    path_true = f"results_py/true_graphs/{graph}.p"
    g_true = pickle.load(open(path_true, "rb"))
    d = len(g_true.nodes)
    n = d - 1
    target = "1"
    for size in sizes:
        for alg in algs:
            path_est = f"results_py/{alg}/graphs/{graph}_{size}_obs.p"
            g_est = pickle.load(open(path_est, "rb"))
            true_dseps = d_separation(g_true, target)
            est_dseps = d_separation(g_est, target)
            # now compare every entry
            tp = 0
            tn = 0
            fp = 0
            fn = 0
            for i in range(true_dseps.shape[0]):
                for j in range(true_dseps.shape[1]):
                    if true_dseps.iloc[i, j] == est_dseps.iloc[i, j]:
                        if true_dseps.iloc[i, j] is True:
                            tp += 1
                        else:
                            tn += 1
                    else:
                        if true_dseps.iloc[i, j] is True:
                            fn += 1
                        else:
                            fp += 1
            d_separated_total = tp + fn
            d_connected_total = tn + fp
            # share of dseps (just make a note, if d-separations were approximated via mc)
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
            content = [f"{graph}_{size}_obs", target, d, alg, "n/a", d_separated_total, d_connected_total,
                       dsep_share, tp, tn, fp, fn, TP_rate, TN_rate, FP_rate, FN_rate, precision, recall, F1]
            # fill evaluation table with current run
            graph_evaluation.loc[len(graph_evaluation)] = content
            graph_evaluation.to_csv("results_py/graph_evaluation.csv", index=False)

for graph in graphs_mc:
    path_true = f"results_py/true_graphs/{graph}.p"
    g_true = pickle.load(open(path_true, "rb"))
    d = len(g_true.nodes)
    n = d - 1
    probs = []
    for jj in range(n):
        probs.append((sp.comb(n - 1, jj)) / (2 ** (n - 1)))
    target = "1"
    predictors = list(g_true.nodes)
    # sort list to get consistent results across different graphs learned on same features (when using mc)
    predictors.sort()
    # remove the target from list of predictors
    predictors.remove(target)
    mc = 100000
    for size in sizes:
        for alg in algs:
            path_est = f"results_py/{alg}/graphs/{graph}_{size}_obs.p"
            g_est = pickle.load(open(path_est, "rb"))
            d_seps_true = []
            d_seps_est = []
            k = 0
            while k < mc:
                predictors = list(g_true.nodes)
                # sort list to get consistent results across different graphs learned on same features (when using mc)
                predictors.sort()
                # remove the target from list of predictors
                predictors.remove(target)
                # draw index for feature of interest
                ind = random.randint(0, n - 1)
                # retrieve feature of interest
                node = predictors[ind]
                # list of all features but feature of interest
                deconfounders = predictors
                deconfounders.remove(node)
                # sample a conditioning set from deconfounders
                # draw a cardinality
                card = np.random.choice(np.arange(n), p=probs)
                if card == 0:
                    # test d-separation with empty set as conditioning set
                    cond_set = set()
                    d_seps_true.append(nx.d_separated(g_true, {node}, {target}, cond_set))
                    d_seps_est.append(nx.d_separated(g_est, {node}, {target}, cond_set))

                else:
                    # draw as many as 'card' numbers from range(n-1) as indices for conditioning set
                    indices = rng.choice(n - 1, size=card, replace=False)
                    cond_set = set()
                    for ii in range(len(indices)):
                        # index for first
                        index = indices[ii]
                        cond_set.add(deconfounders[index])
                    d_seps_true.append(nx.d_separated(g_true, {node}, {target}, cond_set))
                    d_seps_est.append(nx.d_separated(g_est, {node}, {target}, cond_set))
                k += 1

            tp = 0
            tn = 0
            fp = 0
            fn = 0
            for i in range(len(d_seps_true)):
                if d_seps_true[i] == d_seps_est[i]:
                    if d_seps_true[i] is True:
                        tp += 1
                    else:
                        tn += 1
                else:
                    if d_seps_true[i] is True:
                        fn += 1
                    else:
                        fp += 1
            d_separated_total = tp + fn
            d_connected_total = tn + fp
            # share of dseps (just make a note, if d-separations were approximated via mc)
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
            content = [f"{graph}_{size}", target, d, alg, mc, d_separated_total, d_connected_total,
                       dsep_share, tp, tn, fp, fn, TP_rate, TN_rate, FP_rate, FN_rate, precision, recall, F1]
            # fill evaluation table with current run
            graph_evaluation.loc[len(graph_evaluation)] = content
            graph_evaluation.to_csv("results_py/graph_evaluation.csv", index=False)
