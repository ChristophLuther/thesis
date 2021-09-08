# Use set.seed(1902), execute code separately for every data set and reset R after each execution
# for reproducibility of results

# R template for Bayesian network structure learning using bnlearn packages
setwd("/Users/christoph/Desktop/Code")
# install.packages("bnlearn")
library("bnlearn")

set.seed(1902)

# TODO (mby) get cpu name

# load data
df <- read.csv("data/survey/survey_xl.csv")

# as.factor() required for bnlearn.hc()
for (i in colnames(df)){
  df[,i] <- as.factor(df[,i]) 
}
# df[,'a'] <- as.factor(df[,'a']) 

# structure learning (hc or tabu) and wall time
runtime <- system.time({ bn <- tabu(df) })
runtime <- runtime["elapsed"]
line <- "runtime in s - survey data - n=1,000,000 - tabu:"
# file runtime.txt has to exist (or be created at this point)
write(line,file="bnlearnR/results/tabu/runtime.txt",append=TRUE)
write(runtime,file="bnlearnR/results/tabu/runtime.txt",append=TRUE)

# adjacency matrix
adj_mat <- amat(bn)
write.csv(adj_mat, file="bnlearnR/results/tabu/est_amat/survey_xl.csv", row.names = FALSE)

# clear workspace 
rm(list = ls(all.names = TRUE))
