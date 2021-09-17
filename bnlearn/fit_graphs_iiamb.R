# Bayesian network structure learning using inter-iamb algorithm (as implemented in bnlearn)
#setwd("~/thesis_code")
dir.create("bnlearn/results")
dir.create("bnlearn/results/iiamb")
dir.create("bnlearn/results/iiamb/est_amat")
#install.packages("bnlearn")
library("bnlearn")

# set seed
set.seed(1902)

# to loop through different data sets
graphs_discrete <- c("alarm", "asia", "hepar", "sachs")
sizes <- c("s", "m", "l", "xl")
sample_sizes <- c(1000, 10000, 100000, 1000000)

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
    
    # as.factor() required for bnlearn.inter.iamb()
    for (j in colnames(df)){
      df[,j] <- as.factor(df[,j]) 
    }
    
    # structure learning and wall time
    runtime <- system.time({ bn <- inter.iamb(df) })
    runtime <- runtime["elapsed"]
    table[nrow(table) + 1,] = c(i, sample_size, "inter iamb", runtime)
    
    # adjacency matrix
    adj_mat <- amat(bn)
    amat_file <- paste("bnlearn/results/iiamb/est_amat/", i, "_", size, ".csv", sep="")
    write.csv(adj_mat, file=amat_file, row.names = FALSE)
  }
}


# save table
write.csv(table,"bnlearn/results/iiamb/runtime_data_discrete.csv", row.names = FALSE)

