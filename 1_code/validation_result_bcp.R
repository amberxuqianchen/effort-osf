setwd("../")
outputresult <- "./3_output/results/bcp"
datafolder <- "./2_pipeline/tmp"
library("bcp")
library("ggplot2")
library("dplyr")

dfus <- read.csv(file.path(datafolder, "dfus_ussr.csv"))
dfchi <- read.csv(file.path(datafolder, "dfchi_ussr.csv"))
set.seed(101)
# only keep year >= 1920
dfus <- dfus[dfus$year >= 1920,]
# For US
fit <- bcp(dfus[['SovietUnion_vir_vic_diff']])
year_prob <- cbind(dfus$year, fit$posterior.prob,fit$posterior.mean)
colnames(year_prob) <- c("Year", "Prob","Means")
df_year_prob = as.data.frame(year_prob) %>% arrange(desc(Prob))
write.csv(df_year_prob,file.path(outputresult,paste('ussr_us',".csv",sep = "")))
# for China
fit <- bcp(dfchi[['SovietUnion_vir_vic_diff']])
year_prob <- cbind(dfchi$year, fit$posterior.prob,fit$posterior.mean)
colnames(year_prob) <- c("Year", "Prob","Means")
df_year_prob = as.data.frame(year_prob) %>% arrange(desc(Prob))
write.csv(df_year_prob,file.path(outputresult,paste('ussr_chi',".csv",sep = "")))