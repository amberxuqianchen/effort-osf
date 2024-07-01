setwd("/home/local/PSYCH-ADS/xuqian_chen/Github/effort")
preprocessedfolder <- "./2_pipeline/preprocessed"
datafolder <- "./2_pipeline/out"

# Load libraries
library(forecast)
library(tseries)

dfus <- read.csv(file.path(datafolder,"merged_us.csv"))
dfchi <- read.csv(file.path(datafolder,"merged_chi.csv"))
dfus_effort_sentiment <- read.csv(file.path(preprocessedfolder,"sentiments_effort.csv"))
dfchi_effort_sentiment <- read.csv(file.path(preprocessedfolder,"sentiments_effort_chi.csv"))
dfus_efficiency_sentiment <- read.csv(file.path(preprocessedfolder,"sentiments_efficiency.csv"))
dfchi_efficiency_sentiment <- read.csv(file.path(preprocessedfolder,"sentiments_efficiency_chi.csv"))

# merge by year and Year; left by year, right by Year
dfus_efficiency_sentiment$year <- as.numeric(dfus_efficiency_sentiment$Year)
dfus_effort_sentiment$year <- as.numeric(dfus_effort_sentiment$Year)
dfchi_efficiency_sentiment$year <- as.numeric(dfchi_efficiency_sentiment$Year)
dfchi_effort_sentiment$year <- as.numeric(dfchi_effort_sentiment$Year)

df_efficiency_us <- merge(dfus, dfus_efficiency_sentiment, by = 'year')
df_effort_us <- merge(dfus, dfus_effort_sentiment,  by = 'year')
df_efficiency_chi <- merge(dfchi, dfchi_efficiency_sentiment,  by = 'year')
df_effort_chi <- merge(dfchi, dfchi_effort_sentiment,  by = 'year')

# perform auto.arima with sentiment as exogenous variable
auto.arima_sentiment <- function(dfraw, dependent, exogenous){

    # # only keep useful columns
    df <- dfraw[, c("year", dependent, exogenous)]
    df <- df[complete.cases(df),]
    ts <- ts(df[,dependent], start = min(df$year), end = max(df$year), frequency = 1)
    ts_exogenous <- ts(df[,exogenous], start = min(df$year), end = max(df$year), frequency = 1)
    fit <- auto.arima(ts, xreg = ts_exogenous)
    
    # # Extract the coefficient for the exogenous variable and its p-value
    # # Calculate standard error, z-values and p-values
    coef <- fit$coef['xreg']
    standard_error <- sqrt(diag(vcov(fit)))['xreg']
    z_values <- fit$coef['xreg'] / standard_error
    p_value <- 2 * (1 - pnorm(abs(z_values)))


    cat(sprintf("The effect of %s on %s is %s with a p-value of %.3f\n\n", exogenous, dependent, coef, p_value))



    return(fit)
}

# US
print("US")
fit_us_efficiency_sentiment <- auto.arima_sentiment(df_efficiency_us, "efficiency_vir_vic_diff.x", "MeanCompound")
# summary(fit_us_efficiency_sentiment)

fit_us_effort_sentiment <- auto.arima_sentiment(df_effort_us, "effort_vir_vic_diff.x", "MeanCompound")
# summary(fit_us_effort_sentiment)

# China
print("China")
fit_chi_efficiency_sentiment <- auto.arima_sentiment(df_efficiency_chi, "efficiency_vir_vic_diff", "AverageSentiment")
# summary(fit_chi_efficiency_sentiment)
fit_chi_effort_sentiment <- auto.arima_sentiment(df_effort_chi, "effort_vir_vic_diff", "AverageSentiment")
# summary(fit_chi_effort_sentiment)

