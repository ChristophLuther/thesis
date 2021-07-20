# Causal Structure Learning (hc from bnlearn package)
import pandas as pd
import bnlearn as bn
import networkx as nx
import pickle
import time

graph = "survey"
n = 1000
df = pd.read_csv(f"Code/data/csv/{graph}.csv")
df = df[0:n]
start_time = time.time()
model = bn.structure_learning.fit(df)
run_time = time.time() - start_time
adj_mat = model["adjmat"]
mapping = {False: 0, True: 1}
col_names = adj_mat.columns.tolist()
for i in col_names:
    adj_mat[i] = adj_mat.replace({i: mapping})[i]
g = nx.DiGraph(adj_mat)
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
