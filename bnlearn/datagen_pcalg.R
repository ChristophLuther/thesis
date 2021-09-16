# graph generation with pcalg package

setwd("~/Desktop/thesis_code")
dir.create("data/dag_s")
dir.create("data/dag_m")
dir.create("data/dag_l")
dir.create("data/dag_xl")

# install packages if necessary 
# if (!requireNamespace("BiocManager", quietly = TRUE))
#  install.packages("BiocManager")
# BiocManager::install("graph")
# install.packages('pcalg')

# load package 'pcalg'
library('pcalg')

# set seed
set.seed(1902)

# number of nodes for small to large graph
size = c(10, 50, 100)

# probabilities for each pair of nodes to share an edge
probs = c(2/9, 3/49, 3/99)

# names of graphs
size_tokens = c("s", "m", "l")

for (i in c(1:3)){
  
  p = size[i]
  prob = probs[i]
  token = size_tokens[i]
  
  # randomly generate DAG
  graph <- r.gauss.pardag(p, prob=prob, top.sort = FALSE, normalize = FALSE,
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
  
  # create and store another data file for model training
  data_train <- graph$simulate(1000000)
  filename_train <- paste("data/dag_", token, "/dag_", token, "_train.csv", sep="")
  write.csv(data_train, filename_train, row.names = FALSE)
  
  data_test <- graph$simulate(1000000)
  filename_test <- paste("data/dag_", token, "/dag_", token, "_train.csv", sep="")
  write.csv(data_test, filename_test, row.names = FALSE)
  
}

# Run on Sep 15 approx 5:10 pm to 5:55 pm, Error: vector memory exhausted (limit reached?) for
# dgg_xl_1000000_obs -> file missing