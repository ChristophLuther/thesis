# data generation from bn object (cf. bnlearn package)
library('bnlearn')

# sample data from graph, bn object from respective R environment available at
# https://www.bnlearn.com/bnrepository/

load('graph_env/water.rda')

# ran 7/25/21 w/ seed 1902 (for included graphs; refresh b/w runs for reproducibility)
set.seed(1902)

data_xl <- rbn(bn, n=1000000)
data_l <- data_xl[sample(nrow(data_xl), 100000), ]
data_m <- data_xl[sample(nrow(data_xl), 10000), ]
data_s <- data_xl[sample(nrow(data_xl), 1000), ]

write.csv(data_s,"data/water/water_s.csv", row.names = FALSE)
write.csv(data_m,"data/water/water_m.csv", row.names = FALSE)
write.csv(data_l,"data/water/water_l.csv", row.names = FALSE)
write.csv(data_xl,"data/water/water_xl.csv", row.names = FALSE)

adj_mat <- amat(bn)
write.csv(adj_mat, file="true_amat/water.csv", row.names = FALSE)

# clear workspace 
rm(list = ls(all.names = TRUE))
