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
  
  data <- rbn(bn, n=100000)

  filename <- paste("data/train/", i, "_train.csv", sep="")
  
  write.csv(data, filename, row.names = FALSE)
  
}
