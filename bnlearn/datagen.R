# data generation from bn object (cf. bnlearn package)
# set wd to first level of project 
setwd("~/Desktop/thesis_code")
library('bnlearn')
set.seed(1902)
# sample data from graph, bn object from respective R environment available at
# https://www.bnlearn.com/bnrepository/

names <- c("alarm", "asia", "healthcare", "hepar", "mehra", "sangiovese", "sachs")

for (i in names){
  
  env_name <- paste("bnlearn/graph_env/", i, ".rda", sep="")
  load(env_name)

  data_xl <- rbn(bn, n=1000000)
  data_l <- rbn(bn, n=100000)
  data_m <- rbn(bn, n=10000)
  data_s <- rbn(bn, n=1000)
  
  filename_s <- paste("data/", i, "/", i, "_s.csv", sep="")
  filename_m <- paste("data/", i, "/", i, "_m.csv", sep="")
  filename_l <- paste("data/", i, "/", i, "_l.csv", sep="")
  filename_xl <- paste("data/", i, "/", i, "_xl.csv", sep="")
  
  write.csv(data_s, filename_s, row.names = FALSE)
  write.csv(data_m, filename_m, row.names = FALSE)
  write.csv(data_l, filename_l, row.names = FALSE)
  write.csv(data_xl, filename_xl, row.names = FALSE)

  adj_mat <- amat(bn)
  amat_file <- paste("true_amat/", i, ".csv", sep="")
  write.csv(adj_mat, file="amat_file", row.names = FALSE)

  # clear workspace 
}
