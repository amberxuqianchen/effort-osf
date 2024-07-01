# This script is finalized for autoarima and granger results.
# source: https://towardsdatascience.com/a-quick-introduction-on-granger-causality-testing-for-time-series-analysis-7113dc9420d2
setwd("/home/local/PSYCH-ADS/xuqian_chen/Github/effort")
datafolder <- "./2_pipeline/out"
arimafolder <- "./3_output/results/arima"
grangerfolder <- "./3_output/results/granger"
if (!dir.exists(arimafolder)) {
  dir.create(arimafolder)
}
if (!dir.exists(grangerfolder)) {
  dir.create(grangerfolder)
}
# auto.arima
# install.packages("forecast", dependencies = TRUE)
library(forecast)
library(tseries)
# Granger test
library(lmtest)
library(zoo)
library(stargazer)
# VAR
library(vars)

dfus <- read.csv(file.path(datafolder,"merged_us_deletemissing.csv"))
dfchi <- read.csv(file.path(datafolder,"merged_chi_deletemissing.csv"))

# transform GPD per capita to log scale
dfus$gdp_per_capita_log <- log(dfus$GDP.per.capita)
dfchi$gdp_per_capita_log <- log(dfchi$GDP.per.capita)
dfus$gdp_per_capita_z <- scale(dfus$gdp_per_capita_log)
dfchi$gdp_per_capita_z <- scale(dfchi$gdp_per_capita_log)
# loop through dependent variables to run ARIMA, granger causality, and plot
dfus$effort <- dfus$effort_virtue - dfus$effort_vice
dfus$efficiency <- dfus$efficiency_virtue - dfus$efficiency_vice
dfus$InefficientEffort <- dfus$effort_virtue - dfus$efficiency_virtue
dfchi$effort <- dfchi$effort_virtue - dfchi$effort_vice
dfchi$efficiency <- dfchi$efficiency_virtue - dfchi$efficiency_vice
dfchi$InefficientEffort <- dfchi$effort_virtue - dfchi$efficiency_virtue


dfus$indi_z <- as.vector(scale(dfus$indi))
dfchi$indi_z <-  as.vector(scale(dfchi$indi))
dfus$coll_z <-  as.vector(scale(dfus$coll))
dfchi$coll_z <-  as.vector(scale(dfchi$coll))
dfus$loose_z <-  as.vector(scale(dfus$loose))
dfchi$loose_z <-  as.vector(scale(dfchi$loose))
dfus$tight_z <-  as.vector(scale(dfus$tight))
dfchi$tight_z <-  as.vector(scale(dfchi$tight))

# ivs <- c("indi","coll")
ivs <- c("indi_z","coll_z","loose_z","tight_z")
dvs <- c("effort","efficiency","InefficientEffort")
gdp_var <- "gdp_per_capita_z"


########
# Notes#
########
# non_seasonal_ar_order = model_fit$arma[1]
# non_seasonal_ma_order = model_fit$arma[2]

# seasonal_ar_order = model_fit$arma[3]
# seasonal_ma_order = model_fit$arma[4]

# period_of_data = model_fit$arma[5] # 1 for is non-seasonal data

# non_seasonal_diff_order = model_fit$arma[6]
# seasonal_diff_order =  model_fit$arma[7]
# ANOTHER WAY TO GET THE ORDER:
# arimaorder(fit)


# Define the function to perform ARIMA modeling
perform_arima <- function(y_ts, x_ts ,x_name,gdp_var= NULL) {
  if (!is.null(gdp_var)) {
    # Perform ARIMA with exogenous variable (GDP per capita)
    xreg <- cbind(gdp_var, x_ts)
    fit <- auto.arima(y_ts, xreg = xreg)
    ar <- fit$arma[1]
    ma <- fit$arma[2]
    diff <- fit$arma[6]
    model <- arima(y_ts, order = c(ar, diff, ma), xreg = xreg)
    
    # Label the variable names in the model coefficients
    names(model$coef)[names(model$coef) == "gdp_var"] <- "GDP per capita"
    names(model$coef)[names(model$coef) == "x_ts"] <- x_name
    
    result <- list(model = model, ar = ar, diff = diff, ma = ma)
  } else {
    # Perform ARIMA without exogenous variable
    xreg <- cbind(x_ts)
    fit <- auto.arima(y_ts,xreg = xreg)
    ar <- fit$arma[1]
    ma <- fit$arma[2]
    diff <- fit$arma[6]
    model <- arima(y_ts, xreg = xreg, order = c(ar, diff, ma))
    # Label the variable names in the model coefficients
    names(model$coef)[names(model$coef) == "xreg"] <- x_name

    result <- list(model = model, ar = ar, diff = diff, ma = ma)
  }
  return(result)
}

# Define the function to perform Granger causality test
perform_granger_test <- function(iv, dv) {
  # Combine the series into a data frame
  df <- data.frame(y = dv, x = iv)
  
  # Remove rows with NA values
  df <- df[complete.cases(df), ]
  
  # Determine the best order for the VAR model using AIC
  var_result <- VARselect(df, lag.max = 10, type = "both")
  optimal_lag <- var_result$selection["AIC(n)"]
  
  # Fit the VAR model
  var_model <- VAR(df, p = optimal_lag)
  
  # Perform Granger causality test using the estimated VAR model
  granger_test <- causality(var_model, cause = "x")
  p_value <- granger_test$Granger$p.value
  # F-value
  f_value <- granger_test$Granger$statistic[[1]]
  # Degrees of freedom
  df1 <- granger_test$Granger$parameter[[1]]
  df2 <- granger_test$Granger$parameter[[2]]

  result <- list(optimal_lag = optimal_lag, p_value = p_value, f_value = f_value, df1 = df1, df2 = df2)
  return(result)
}
# Function to perform ARIMA and Granger tests for either dfchi or dfus
perform_arima_and_granger <- function(data, ivs, dvs, gdp_var) {
  model_list <- list()
  model_list_GDP <- list()
  model_names <- c()
  model_GDP_names <- c()
  model_results <- data.frame(
    
    Predictor = character(),
    Order_p_d_q = character(),
    Coefficient = numeric(),
    SE = numeric(),
    t = numeric(),
    p = numeric(),
    stringsAsFactors = FALSE
  )
  model_GDP_results <- data.frame(
    Predictor = character(),
    Order_p_d_q = character(),
    Coefficient = numeric(),
    SE = numeric(),
    t = numeric(),
    p = numeric(),
    stringsAsFactors = FALSE
  )
granger_results <- data.frame(
  IV = character(),
  DV = character(),
  best_lag = numeric(),
  F_value = character(),
  p_value = numeric(),
  reverse_F_value = character(),
  reverse_p_value = numeric(),
  stringsAsFactors = FALSE
)
  
  for (j in 1:length(dvs)) {
    for (i in 1:length(ivs)) {
      x_ts <- ts(data[, ivs[i]])
      y_ts <- ts(data[, dvs[j]])
      gdp_ts <- ts(data[[gdp_var]])
      
      # Perform ARIMA with GDPpc as controlling variable
      arima_result <- perform_arima(y_ts, x_ts = x_ts, x_name = ivs[i], gdp_var = gdp_ts)
      
      # Save the model
      model_name <- paste(dvs[j], " (", arima_result$ar, ",", arima_result$diff, ",", arima_result$ma, ")", sep = "")
      model_list_GDP[[paste(dvs[j], "~", ivs[i])]] <- arima_result$model
      model_GDP_names <- c(model_GDP_names, model_name)
      # Calculate standard error, z-values and p-values
      standard_error <- sqrt(diag(vcov(arima_result$model)))['x_ts']
      z_values <- arima_result$model$coef[ivs[i]] / standard_error
      p_values <- 2 * (1 - pnorm(abs(z_values)))
      model_GDP_results <- rbind(model_GDP_results,
                             data.frame(
                               Predictor = ivs[i],
                               Order_p_d_q = paste("(", arima_result$ar, ", ", arima_result$diff, ", ", arima_result$ma, ")", sep = ""),
                               Coefficient = round(coef(arima_result$model)[ivs[i]],3),
                               SE = round(standard_error,3),
                               t = round(z_values,3),
                               p = round(p_values,3)
                             ))

      # Perform ARIMA without GDPpc as controlling variable
      arima_result <- perform_arima(y_ts, x_ts = x_ts, x_name = ivs[i], gdp_var = NULL)
      
      # Save the model
      model_name <- paste(dvs[j], " (", arima_result$ar, ",", arima_result$diff, ",", arima_result$ma, ")", sep = "")
      model_names <- c(model_names, model_name)
      model_list[[paste(dvs[j], "~", ivs[i])]] <- arima_result$model
      
      # Calculate standard error, z-values and p-values
      standard_error <- sqrt(diag(vcov(arima_result$model)))['xreg']
      z_values <- arima_result$model$coef[ivs[i]] / standard_error
      p_values <- 2 * (1 - pnorm(abs(z_values)))
      model_results <- rbind(model_results,
                             data.frame(
                               Predictor = ivs[i],
                               Order_p_d_q = paste("(", arima_result$ar, ", ", arima_result$diff, ", ", arima_result$ma, ")", sep = ""),
                                Coefficient = round(coef(arima_result$model)[ivs[i]],3),
                                SE = round(standard_error,4),
                                t = round(z_values,4),
                                p = round(p_values,4)
                             ))

      # Perform Granger causality test for y~x
        granger_result_yx <- perform_granger_test(x_ts, y_ts)

        # Perform Granger causality test for x~y
        granger_result_xy <- perform_granger_test(y_ts, x_ts)

        granger_results <- rbind(granger_results,
                         data.frame(
                           IV = ivs[i],
                           DV = dvs[j],
                           best_lag = granger_result_yx$optimal_lag,
                           F_value = paste("F(", granger_result_yx$df1, ", ", granger_result_yx$df2, ") = ", round(granger_result_yx$f_value,2), sep = ""),
                           p_value = granger_result_yx$p_value,
                           reverse_F_value = paste("F(", granger_result_xy$df1, ", ", granger_result_xy$df2, ") = ", round(granger_result_xy$f_value,2), sep = ""),
                           reverse_p_value = granger_result_xy$p_value
                         )
)
      
    }
  }
  
  return(list(model_list, model_list_GDP, model_names, model_GDP_names, granger_results,model_results,model_GDP_results))
}

# Call the function for dfchi

results_chi <- perform_arima_and_granger(dfchi, ivs, dvs, gdp_var)

# Extract the results
model_list_chi <- results_chi[[1]]
model_list_GDP_chi <- results_chi[[2]]
model_names_chi <- results_chi[[3]]
model_GDP_names_chi <- results_chi[[4]]
granger_results_chi <- results_chi[[5]]
model_results <- results_chi[[6]]
model_GDP_results <- results_chi[[7]]
# Save the granger_results to a .csv file
write.csv(granger_results_chi, file = file.path(grangerfolder, "diff_granger_results_chi_deletemissing.csv"), row.names = FALSE)
write.csv(model_results, file = file.path(arimafolder, "arima_model_results_chi_deletemissing.csv"), row.names = FALSE)
write.csv(model_GDP_results, file = file.path(arimafolder, "arima_model_GDP_results_chi_deletemissing.csv"), row.names = FALSE)
# Save the model results
stargazer(model_list_chi, summary = FALSE, type = "text", column.labels = model_names_chi, star.cutoffs = c(0.05, 0.01, 0.001),title = "ARIMA Results for China", out = file.path(arimafolder, "arima_model_Culturalz_chi_deletemissing.txt"))
stargazer(model_list_GDP_chi, summary = FALSE, type = "text", column.labels = model_GDP_names_chi, star.cutoffs = c(0.05, 0.01, 0.001),title = "ARIMA Results (including GDP) for China", out = file.path(arimafolder, "arima_model_GDPz_Culturalz_chi_deletemissing.txt"))

# Call the function for dfus
results_us <- perform_arima_and_granger(dfus, ivs, dvs, gdp_var)

# Extract the results
model_list_us <- results_us[[1]]
model_list_GDP_us <- results_us[[2]]
model_names_us <- results_us[[3]]
model_GDP_names_us <- results_us[[4]]
granger_results_us <- results_us[[5]]
model_results <- results_us[[6]]
model_GDP_results <- results_us[[7]]
# Save the model results
write.csv(granger_results_us, file = file.path(grangerfolder, "diff_granger_results_us_deletemissing.csv"), row.names = FALSE)
write.csv(model_results, file = file.path(arimafolder, "arima_model_results_us_deletemissing.csv"), row.names = FALSE)
write.csv(model_GDP_results, file = file.path(arimafolder, "arima_model_GDP_results_us_deletemissing.csv"), row.names = FALSE)
stargazer(model_list_us, summary = FALSE, ci = TRUE,type = "text", column.labels = model_names_us, star.cutoffs = c(0.05, 0.01, 0.001), title = "ARIMA Results for US", out = file.path(arimafolder, "arima_model_Culturalz_us_deletemissing.txt"))
stargazer(model_list_GDP_us, summary = FALSE, type = "text", column.labels = model_GDP_names_us, star.cutoffs = c(0.05, 0.01, 0.001), title = "ARIMA Results (including GDP) for US", out = file.path(arimafolder, "arima_model_GDPz_Culturalz_us_deletemissing.txt"))
ci_list <- lapply(model_list_GDP_us, function(x) confint(x, level = 0.95))
stargazer(model_list_GDP_us, type = "text", ci.levels = 0.95, ci = TRUE)
# perform ARIMA with GDP as predictor and dvs as outcome
dfus$gdp_z <- scale(dfus$GDP.per.capita)
dfchi$gdp_z <- scale(dfchi$GDP.per.capita)
model_list_GDP <- list()
model_GDP_names <- c()
for (j in 1:length(dvs)){
  y_ts <- ts(dfus[,dvs[j]])
  gdp_ts <- ts(dfus$gdp_z)
  # run ARIMA with GDPpc as controlling variable
  xreg <- cbind(gdp_ts)
  fit <- auto.arima(y_ts,xreg = xreg)
  ar <- fit$arma[1]
  ma <- fit$arma[2]
  diff <- fit$arma[6]
  model <- arima(y_ts,order = c(ar,diff,ma),xreg = xreg)

  # lable the ivnames
  names(model$coef)[names(model$coef) == "gdp_ts"] <- "GDP per capita"
  # save the model
  model_name <- paste(dvs[j], " (", ar, ",", diff, ",", ma, ")", sep="")
  model_GDP_names <- c(model_GDP_names,model_name)
  model_list_GDP[[paste(dvs[j],"~","GDP")]] <- model

}

stargazer(model_list_GDP,summary = FALSE,type = "text",column.labels = model_GDP_names,star.cutoffs = c(0.05,0.01,0.001), title = "ARIMA Results (only GDP) for US",out = file.path(arimafolder,"arima_model_onlyGDP_us.txt"))
model_list_GDP <- list()
model_GDP_names <- c()
for (j in 1:length(dvs)){
  y_ts <- ts(dfchi[,dvs[j]])
  gdp_ts <- ts(dfchi$gdp_z)
  # run ARIMA with GDPpc as controlling variable
  xreg <- cbind(gdp_ts)
  fit <- auto.arima(y_ts,xreg = xreg)
  ar <- fit$arma[1]
  ma <- fit$arma[2]
  diff <- fit$arma[6]
  model <- arima(y_ts,order = c(ar,diff,ma),xreg = xreg)

  # lable the ivnames
  names(model$coef)[names(model$coef) == "gdp_ts"] <- "GDP per capita"
  # save the model
  model_name <- paste(dvs[j], " (", ar, ",", diff, ",", ma, ")", sep="")
  model_GDP_names <- c(model_GDP_names,model_name)
  model_list_GDP[[paste(dvs[j],"~","GDP")]] <- model
}
stargazer(model_list_GDP,summary = FALSE,type = "text",column.labels = model_GDP_names,star.cutoffs = c(0.05,0.01,0.001), title = "ARIMA Results (only GDP) for China",out = file.path(arimafolder,"arima_model_onlyGDP_chi.txt"))