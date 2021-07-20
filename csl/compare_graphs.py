# Complete code to count the number of TP/FP/TN/FN d-separation statements from an estimated graph compared to its
# ground truth graph
import pickle
from comparison import GraphComparison
import pandas as pd

# in case I want to loop through graph names
# names = ["alarm","asia","child","hail","hepar","insurance","mildew","sachs","survey",]
# targets = {"alarm": "CATECHOL","asia": "dysp","barley": "spndx","child": "XrayReport","hail": "R5Fcst",
# "hepar": "Cirrhosis","insurance": "PropCost","mildew": "udbytte","sachs": "Akt","survey": "T","water" : "TBD"}
graph_name = "survey"
n = 1
# example with survey graph (exact)
path_true = f"Code/data/graphs/true/{graph_name}_true_graph.p"
# path to estimated graph
path_est = f"Code/data/graphs/estimated/{graph_name}/{n}k.p"
# load true graph
g_true = pickle.load(open(path_true, "rb"))
# load estimated graph
g_est = pickle.load(open(path_est, "rb"))

# if mc necessary, do not forget mc and random state
mc = "n/a"
# target node
target_node = "T"
# instance
survey_comp = GraphComparison(g_true, g_est, target_node)

# true total and false total are ground truth
TP, TN, FP, FN, true_total, false_total = survey_comp.exact()

# What do I finally need? A dataframe with all the necessary info (Overall)
# target (already at the beginning)
# number of nodes
d = len(g_true.nodes)
# potential d-separations w.r.t. y
potential_dseps = (d-1) * (2**(d-2))
# true number of dseps (see above: true_total)
# share of dseps (just make a node, if d-separations were approximated via mc)
dsep_share = true_total/(true_total+false_total)
# and don't forget to mention the number of

# graph specific table
# then TP-, TN-, FP-, and FN-rate as above
TP_rate = TP/true_total
FN_rate = FN/true_total
TN_rate = TN/false_total
FP_rate = FP/false_total

# F1 score
precision = TP / (TP+FP)
recall = TP_rate
F1 = (2 * precision * recall)/(precision + recall)

try:
    evaluation_table = pd.read_csv(
        "Code/data/graphs/evaluation_table.csv",
        index=False,
    )
except:
    col_names = [
        "graph",
        "target",
        "d",
        "potential_dseps",
        "n (during learning)",
        "MC",
        "ground truth d-separations",
        "ground truth d-connections",
        "d-sep share",
        "TP",
        "TN",
        "FP",
        "FN",
        "TP rate",
        "TN rate",
        "FP rate",
        "FN rate",
        "precision",
        "recall",
        "F1"
    ]
    evaluation_table = pd.DataFrame(columns=col_names)

content = [graph_name, target_node, d, potential_dseps, n, mc, true_total, false_total, dsep_share,
           TP, TN, FP, FN, TP_rate, TN_rate, FP_rate, FN_rate, precision, recall, F1]
# fill evaluation table with current run
evaluation_table.loc[len(evaluation_table)] = content

evaluation_table.to_csv(
    "Code/data/graphs/evaluation_table.csv", index=False
)
