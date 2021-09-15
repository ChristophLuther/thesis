# Bayesian network structure learning using bnlearn package
setwd("/Users/christoph/Desktop/thesis_code")

#install.packages("bnlearn")
library("bnlearn")

# set seed
set.seed(1902)

# to loop through different data sets
graphs_discrete <- c("alarm", "asia", "hepar", "sachs")
graphs_cont <- c("dag_s", "dag_m", "dag_l", "dag_xl")
sizes <- c("s", "m", "l", "xl")
sample_sizes <- (1000, 10000, 100000, 1000000)

# initiate data frame to store metadata like runtime
table <- data.frame(matrix(ncol = 4, nrow = 0))
col_names <- c("Graph", "n sample size", "algorithm", "runtime in s")
colnames(table) <- col_names

for (i in graphs_discrete){
  
  for (k in c(1:4)){
    
    size <- sizes[k]
    sample_size <- sample_sizes[k]
    # load data
    filename <- paste("data/", i, "/", i, "_", size, ".csv", sep="")
    df <- read.csv(filename)
    
    # as.factor() required for bnlearn.tabu()
    for (j in colnames(df)){
      df[,j] <- as.factor(df[,j]) 
    }
    
    # structure learning and wall time
    runtime <- system.time({ bn <- tabu(df) })
    runtime <- runtime["elapsed"]
    table[nrow(table) + 1,] = c(i, sample_size, "tabu", runtime)
    
    # adjacency matrix
    adj_mat <- amat(bn)
    amat_file <- paste("bnlearn/results/tabu/est_amat/", i, "_", size, ".csv", sep="")
    write.csv(adj_mat, file=amat_file, row.names = FALSE)
  }
}

for (i in graphs_cont){
  
  for (sample_size in sample_sizes){
    
    # load data
    filename <- paste("data/", i, "/", i, "_", sample_size, "_obs.csv", sep="")
    df <- read.csv(filename)
    
    # if conditions only necessary for the respective graphs (unused)
    if (i == "healthcare"){
      # as.factor() required for bnlearn.tabu()
      for (j in c("A", "C", "H")){
        df[,j] <- as.factor(df[,j]) 
      }
    }
    
    if (i == "mehra"){
      # as.factor() required for bnlearn.tabu()
      for (j in c("Region", "Zone", "Type", "Season", "Year", "Month", "Day", "Hour")){
        df[,j] <- as.factor(df[,j]) 
      }
    }
    
    if (i == "sangiovese"){
      # as.factor() required for bnlearn.tabu()
      for (j in c("Treatment")){
        df[,j] <- as.factor(df[,j]) 
      }
    }
    
    # structure learning and wall time
    runtime <- system.time({ bn <- tabu(df) })
    runtime <- runtime["elapsed"]
    table[nrow(table) + 1,] = c(i, sample_size, "tabu", runtime)
    
    # adjacency matrix
    adj_mat <- amat(bn)
    amat_file <- paste("bnlearn/results/tabu/est_amat/", i, "_", sample_size, "_obs.csv", sep="")
    write.csv(adj_mat, file=amat_file, row.names = FALSE)
  }
}

# save table
write.csv(table,"bnlearn/results/tabu/runtime_data.csv", row.names = FALSE)

