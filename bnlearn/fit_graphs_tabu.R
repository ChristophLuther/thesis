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
    
    # as.factor() required for bnlearn.tabu()
    for (j in colnames(df)){
      df[,j] <- as.factor(df[,j]) 
    }
    
    # structure learning and wall time
    runtime <- system.time({ bn <- tabu(df) })
    runtime <- runtime["elapsed"]
    line <- paste("runtime in sec - data: ", i, " - size: ", size, " - method: tabu:", sep="")
    # file runtime.txt has to exist (or be created at this point)
    write(line,file="bnlearn/results/tabu/runtime.txt",append=TRUE)
    write(runtime,file="bnlearn/results/tabu/runtime.txt",append=TRUE)
    
    # adjacency matrix
    adj_mat <- amat(bn)
    amat_file <- paste("bnlearn/results/tabu/est_amat/", i, "_", size, ".csv", sep="")
    write.csv(adj_mat, file=amat_file, row.names = FALSE)
  }
}

for (i in graphs_cont){
  
  for (size in sizes){
    
    # load data
    filename <- paste("data/", i, "/", i, "_", size, ".csv", sep="")
    df <- read.csv(filename)
    
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
    line <- paste("runtime in sec - data: ", i, " - size: ", size, " - method: tabu:", sep="")
    # file runtime.txt has to exist (or be created at this point)
    write(line,file="bnlearn/results/tabu/runtime.txt",append=TRUE)
    write(runtime,file="bnlearn/results/tabu/runtime.txt",append=TRUE)
    
    # adjacency matrix
    adj_mat <- amat(bn)
    amat_file <- paste("bnlearn/results/tabu/est_amat/", i, "_", size, ".csv", sep="")
    write.csv(adj_mat, file=amat_file, row.names = FALSE)
  }
}
