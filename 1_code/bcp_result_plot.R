
setwd("/home/local/PSYCH-ADS/xuqian_chen/Github/effort")
datafolder <- "./2_pipeline/out"
outputfolder <- "./3_output/plot/bcp"
outputresult <- "./3_output/results/bcp"
if (!dir.exists(outputfolder)) {
  dir.create(outputfolder)
}
if (!dir.exists(outputresult)) {
  dir.create(outputresult)
}

library("bcp")
library("ggplot2")
library("dplyr")

# Helper function for posterior data
getPosteriorData <- function(df, country,colname) {
  fit <- bcp(df[[colname]])
  year_prob <- cbind(df$year, fit$posterior.prob,fit$posterior.mean)
  colnames(year_prob) <- c("Year", "Prob","Means")
  df_year_prob = as.data.frame(year_prob) %>% arrange(desc(Prob))
  write.csv(df_year_prob,file.path(outputresult,paste(country,"_",colname,".csv",sep = "")))
  df_year_prob
}

# Helper function for plot creation

createPlot <- function(df_virtue, df_vice, title, filename, labels=c("Virtue", "Vice")) {
  p <- ggplot() +
    geom_line(data = df_virtue, aes(Year, Means, color = labels[1])) +
    annotate("text", x = df_virtue[1:3,1], y = df_virtue[1:3,3], label = paste(df_virtue[1:3,1], df_virtue[1:3,2], sep = ", "), size = 3) 

  if(!is.null(df_vice)){
    p <- p + 
      geom_line(data = df_vice, aes(Year, Means, color = labels[2])) +
      annotate("text", x = df_vice[1:3,1], y = df_vice[1:3,3], label = paste(df_vice[1:3,1], df_vice[1:3,2], sep = ", "), size = 3) 
  }

  p <- p +
    labs(title = title, x = "Year", y = "Posterior Means", color = "Attitude", 
         caption = "Annotations indicate the top 3 years with the highest posterior probability")

  ggsave(file.path(outputfolder, filename), plot = p, width = 8, height = 6)
}


# Load Data
loadData <- function(filename){
  datapath <- file.path(datafolder, filename)
  df <- read.csv(datapath)
  df <- df[!is.na(df$effort_virtue),]
  df
}

dfus <- loadData("merged_us.csv")
dfchi <- loadData("merged_chi.csv")

set.seed(101)

# For US
dfus$effort<- dfus$effort_virtue - dfus$effort_vice
dfus$efficiency<- dfus$efficiency_virtue - dfus$efficiency_vice

createPlot(getPosteriorData(dfus,"us", "effort"),
            getPosteriorData(dfus,"us", "efficiency"),
            title = "Moral Values of Effort and Efficiency (US)",
            filename = "us_effort_efficiency.png",
            )

createPlot(getPosteriorData(dfus,"us", "effort_virtue"), 
            getPosteriorData(dfus,"us", "efficiency_virtue"), 
            "Effort and Efficiency: Virtue (US)", 
            "effort_efficiency_virtue_us.png", 
            labels=c("Effort", "Efficiency"))

dfus$effort_efficiency_virtue <- dfus$effort_virtue - dfus$efficiency_virtue
createPlot(getPosteriorData(dfus,"us", "effort_efficiency_virtue"), 
            NULL,
            "Effort - Efficiency: Virtue (US)", 
            "effort_efficiency_virtue_diff_us.png", 
            labels=c("Effort - Efficiency"))

# For China
dfchi$effort<- dfchi$effort_virtue - dfchi$effort_vice
dfchi$efficiency<- dfchi$efficiency_virtue - dfchi$efficiency_vice

createPlot(getPosteriorData(dfchi,"chi", "effort"),
            getPosteriorData(dfchi,"chi", "efficiency"),
            "Moral Values of Effort and Efficiency (China)",
            "chi_effort_efficiency.png")

createPlot(getPosteriorData(dfchi,"chi", "effort_virtue"), 
            getPosteriorData(dfchi,"chi", "efficiency_virtue"), 
            "Effort and Efficiency: Virtue (China)", 
            "effort_efficiency_virtue_chi.png", 
            labels=c("Effort", "Efficiency"))

dfchi$effort_efficiency_virtue <- dfchi$effort_virtue - dfchi$efficiency_virtue
createPlot(getPosteriorData(dfchi,"chi", "effort_efficiency_virtue"), 
            NULL,
            "Effort - Efficiency: Virtue (China)", 
            "effort_efficiency_virtue_diff_chi.png", 
            labels=c("Effort - Efficiency"))