# Causal Structure Learning (hc from bnlearn package)
# NOTE: structure learning conducted in R
import pandas as pd
import bnlearn as bn
import networkx as nx
import pickle
import time


graph = "survey"
df = pd.read_csv(f"Code/data/csv/{graph}.csv")
n = len(df)
# start time to track wall time of program
start_time = time.time()
# fit model (see bnlearn documentation for options)
model = bn.structure_learning.fit(df)
# wall time of structure learning
run_time = time.time() - start_time
# get adjacency matrix and remap to 0-1 instead of boolean entries
adj_mat = model["adjmat"]
mapping = {False: 0, True: 1}
col_names = adj_mat.columns.tolist()
for i in col_names:
    adj_mat[i] = adj_mat.replace({i: mapping})[i]
# create nx.DiGraph from adjacency matrix (format required for further processing)
g = nx.DiGraph(adj_mat)
# save graph
sample_size = str(int(n / 1000))
output_file = f"Code/data/graphs/estimated/{graph}/{sample_size}k.p"
pickle.dump(g, open(output_file, "wb"))

# store the times for all runs

try:
    file = open(
        "Code/data/graphs/metadata.txt",
        "a",
    )
    file.write(
        "\n" + f"runtime in sec for {graph}-graph with n = {n} observations: " + str(run_time)
    )
    file.close()

except:
    with open(
            "Code/data/graphs/metadata.txt",
            "w",
    ) as file:
        text_temp = f"runtime in sec for {graph}-graph with n = {n} observations: " + str(run_time)
        text_temp = str(text_temp)
        file.write(text_temp)
