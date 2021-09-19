"""Single file to compare graphs"""
import pickle
import pandas as pd
import random
import numpy as np
import scipy.special as sp
import networkx as nx

# file for comparison
try:
    graph_evaluation = pd.read_csv("results_py/graph_evaluation.csv")
except:
    col_names = ["graph", "target_node", "d", "method", "mc",
                 "true_total", "false_total", "dsep_share", "TP", "TN", "FP", "FN", "TP_rate",
                 "TN_rate", "FP_rate", "FN_rate", "precision", "recall", "F1"]
    graph_evaluation = pd.DataFrame(columns=col_names)

# TODO make inputs: method, graph, target
target = "Cirrhosis"

# get a vector of d-separation statement for true graph
path_true = f"results_py/true_graphs/hepar.p"
g_true = pickle.load(open(path_true, "rb"))
# number of nodes
d = len(g_true.nodes)
# number of predictors
n = d-1
# get a vector of d-separation statement for estimated graph
path_est = f"results_py/hc/graphs/hepar_s.p"
g_est = pickle.load(open(path_est, "rb"))

predictors = list(g_true.nodes)
# sort list to get consistent results across different graphs learned on same features (when using mc)
predictors.sort()
# remove the target from list of predictors
predictors.remove(target)

mc = 1000
# survey_comp = GraphComparison(g_true, g_est, target_node, mc=mc, rand_state=42)
# TP, TN, FP, FN, true_total, false_total = survey_comp.approx()
# if random_state is not None:
random.seed(42)
np.random.seed(42)
rng = np.random.default_rng(seed=42)
# else:
#     rng = np.random.default_rng()
# initiate vector to store True/False for d-separations (cannot track conditioning sets)
d_seps_true = []
d_seps_est = []

# get a vector of probabilities to draw the size of the conditioning set; note that for n-1 potential
# deconfounders there are n different sizes of conditioning sets because of the empty set
probs = []
for i in range(n):
    probs.append((sp.comb(n - 1, i)) / (2 ** (n - 1)))
k = 0
while k < mc:
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
        indices = rng.choice(n - 2, size=card, replace=False)
        cond_set = set()
        for ii in range(len(indices)):
            # index for first
            index = indices[ii]
            cond_set.add(deconfounders[index])
        d_seps_true.append(nx.d_separated(g_true, {node}, {target}, cond_set))
        d_seps_est.append(nx.d_separated(g_est, {node}, {target}, cond_set))
    k += 1
