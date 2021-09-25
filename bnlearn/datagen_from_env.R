# data generation from bn object as from .rda files (cf. https://www.bnlearn.com/bnrepository/)

setwd("~/Desktop/thesis_code")
# directories for graphs (asia, alarm, ...) should exist (as in github repo)
dir.create("data")
dir.create("bnlearn/true_amat")
# install package if necessary
# install.packages('bnlearn')

# load package 'bnlearn'
library('bnlearn')

# set seed
set.seed(1902)

names <- c("alarm", "asia", "hepar", "sachs")

for (i in names){
  
  env_name <- paste("bnlearn/graph_env/", i, ".rda", sep="")
  load(env_name)

  data <- rbn(bn, n=2000000)
  
  filename <- paste("data/", i, ".csv", sep="")

  write.csv(data, filename, row.names = FALSE)
    
  adj_mat <- amat(bn)
  amat_file <- paste("bnlearn/true_amat/", i, ".csv", sep="")
  write.csv(adj_mat, file=amat_file, row.names = FALSE)
}
