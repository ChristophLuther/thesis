"""Evaluate structure learning performance measured by ability to learn d-separations"""
import pickle
from comparison import GraphComparison
import pandas as pd


# in case I want to loop through graph names (for every sample size separately)
names = ["alarm_s", "asia_s", "hepar_s", "sachs_s", "dag_s_1000_obs", "dag_m_1000_obs", "dag_m_1000_obs"]

targets_mid = {"alarm_s": "CVP", "asia_s": "dysp", "hepar_s": "Cirrhosis", "sachs_s": "Erk",
               "dag_s_1000_obs": "V1", "dag_m_1000_obs": "V1", "dag_l_1000_obs": "V1"}

methods = ["iiamb", "gs", "hc", "tabu", "mmhc", "h2pc"]

sample_size = 1000

# read graph evaluation csv or create if not existent
try:
    graph_evaluation = pd.read_csv("results_py/graph_evaluation.csv")
except:
    col_names = ["graph", "target_node", "d", "potential_dseps", "size", "method", "mc",
                 "true_total", "false_total", "dsep_share", "TP", "TN", "FP", "FN", "TP_rate",
                 "TN_rate", "FP_rate", "FN_rate", "precision", "recall", "F1"]
    graph_evaluation = pd.DataFrame(columns=col_names)

for method in methods:
    for graph in names:
        # exact graph
        path_true = f"results_py/true_graphs/{graph}.p"
        # path to estimated graph
        path_est = f"results_py/{method}/graphs/{graph}.p"
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
        content = [graph, target_node, d, potential_dseps, sample_size, method, mc, true_total, false_total, dsep_share,
                   TP, TN, FP, FN, TP_rate, TN_rate, FP_rate, FN_rate, precision, recall, F1]
        # fill evaluation table with current run
        graph_evaluation.loc[len(graph_evaluation)] = content

graph_evaluation.to_csv(
            "results_py/graph_evaluation.csv", index=False
        )
