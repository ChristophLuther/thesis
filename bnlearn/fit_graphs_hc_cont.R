# Bayesian network structure learning using hc algorithm (as implemented in bnlearn)
setwd("~/Desktop/thesis_code")
dir.create("bnlearn/results")
dir.create("bnlearn/results/hc")
dir.create("bnlearn/results/hc/est_amat")

#install.packages("bnlearn")
library("bnlearn")

# set seed
set.seed(1902)

# to loop through different data sets
graphs_cont <- c("dag_s", "dag_m", "dag_l")
sizes <- c("s", "m", "l", "xl")
sample_sizes <- c("1000", "10000", "1e+05", "1e+06")

# initiate data frame to store metadata like runtime
table <- data.frame(matrix(ncol = 4, nrow = 0))
col_names <- c("Graph", "n sample size", "algorithm", "runtime in s")
colnames(table) <- col_names

for (i in graphs_cont){
  
  for (sample_size in sample_sizes){
    
    # load data
    filename <- paste("data/", i, "/", i, "_", sample_size, "_obs.csv", sep="")
    df <- read.csv(filename)
    
    # if conditions only necessary for the respective graphs (unused)
    if (i == "healthcare"){
      # as.factor() required for bnlearn.hc()
      for (j in c("A", "C", "H")){
        df[,j] <- as.factor(df[,j]) 
      }
    }
    
    if (i == "mehra"){
      # as.factor() required for bnlearn.hc()
      for (j in c("Region", "Zone", "Type", "Season", "Year", "Month", "Day", "Hour")){
        df[,j] <- as.factor(df[,j]) 
      }
    }
    
    if (i == "sangiovese"){
      # as.factor() required for bnlearn.hc()
      for (j in c("Treatment")){
        df[,j] <- as.factor(df[,j]) 
      }
    }
    
    # structure learning and wall time
    runtime <- system.time({ bn <- hc(df) })
    runtime <- runtime["elapsed"]
    table[nrow(table) + 1,] = c(i, sample_size, "hc", runtime)
    
    # adjacency matrix
    adj_mat <- amat(bn)
    amat_file <- paste("bnlearn/results/hc/est_amat/", i, "_", sample_size, "_obs.csv", sep="")
    write.csv(adj_mat, file=amat_file, row.names = FALSE)
  }
}

# save table
write.csv(table,"bnlearn/results/hc/runtime_data_cont.csv", row.names = FALSE)

