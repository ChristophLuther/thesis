# graph generation with pcalg package

setwd("~/Desktop/thesis_code")

# install packages if necessary 
# if (!requireNamespace("BiocManager", quietly = TRUE))
#  install.packages("BiocManager")
# BiocManager::install("graph")
# install.packages('pcalg')

# load package 'pcalg'
library('pcalg')

# set seed
set.seed(1902)

# number of nodes for small to extra large graph
size = c(10, 50, 100, 1000)

# probabilities for each pair of nodes to share an edge
probs = c(2/9, 3/49, 3/99, 3/999)

# names of graphs
size_tokens = c("s", "m", "l", "xl")

for (i in c(1:4)){
  
  p = size[i]
  prob = probs[i]
  token = size_tokens[i]
  
  # randomly generate DAG
  dag <- r.gauss.pardag(p, prob=prob, top.sort = FALSE, normalize = FALSE,
                          lbe = 0.1, ube = 5, neg.coef = TRUE, labels = as.character(1:p),
                          lbv = 0.5, ubv = 1)
  
  # get Boolean adjacency matrix and store it
  amat <- as(graph, "matrix")
  amat_name <- paste("bnlearn/true_amat/dag_", token, ".csv", sep="")
  write.csv(amat, amat_name, row.names = FALSE)
  
  # create data sets of four different sizes and store them
  for (j in c(1000, 10000, 100000, 1000000)){
    data <- graph$simulate(j)
    filename <- paste("data/dag_", token, "/dag_", token, "_",  j,"_obs.csv", sep="")
    write.csv(data, filename, row.names = FALSE)
  }
  
  # create and stire another data file for model training
  data <- graph$simulate(1000000)
  filename <- paste("data/dag_", token, "/dag_", token, "_train.csv", sep="")
  write.csv(data, filename, row.names = FALSE)
  
}
