# Bayesian network structure learning using bnlearn package
setwd("/Users/christoph/Desktop/thesis_code")

# install.packages("bnlearn")
library("bnlearn")

set.seed(1902)

graphs_discrete <- c("alarm", "asia", "hepar", "sachs")
graphs_cont <- c("healthcare", "mehra", "sangiovese")

sizes <- c("s", "m", "l", "xl")

for (i in graphs_discrete){
  
  for (size in sizes){
    
    # load data
    filename <- paste("data/", i, "/", i, "_", size, ".csv", sep="")
    df <- read.csv(filename)

    # as.factor() required for bnlearn.hc()
    for (j in colnames(df)){
      df[,j] <- as.factor(df[,j]) 
    }

    # structure learning and wall time
    runtime <- system.time({ bn <- hc(df) })
    runtime <- runtime["elapsed"]
    line <- paste("runtime in sec - data: ", i, " - size: ", size, " - method: hc:", sep="")
    # file runtime.txt has to exist (or be created at this point)
    write(line,file="bnlearn/results/hc/runtime.txt",append=TRUE)
    write(runtime,file="bnlearn/results/hc/runtime.txt",append=TRUE)

    # adjacency matrix
    adj_mat <- amat(bn)
    amat_file <- paste("bnlearn/results/hc/est_amat/", i, "_", size, ".csv", sep="")
    write.csv(adj_mat, file=amat_file, row.names = FALSE)
  }
}

for (i in graphs_cont){
  
  for (size in sizes){
    
    # load data
    filename <- paste("data/", i, "/", i, "_", size, ".csv", sep="")
    df <- read.csv(filename)

    # structure learning and wall time
    runtime <- system.time({ bn <- hc(df) })
    runtime <- runtime["elapsed"]
    line <- paste("runtime in sec - data: ", i, " - size: ", size, " - method: hc:", sep="")
    # file runtime.txt has to exist (or be created at this point)
    write(line,file="bnlearn/results/hc/runtime.txt",append=TRUE)
    write(runtime,file="bnlearn/results/hc/runtime.txt",append=TRUE)
    
    # adjacency matrix
    adj_mat <- amat(bn)
    amat_file <- paste("bnlearn/results/hc/est_amat/", i, "_", size, ".csv", sep="")
    write.csv(adj_mat, file=amat_file, row.names = FALSE)
  }
}
