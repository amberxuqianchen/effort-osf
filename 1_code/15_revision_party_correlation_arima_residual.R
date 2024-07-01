library(forecast)
library(tidyverse)

# Define file paths
script_dir <- dirname('/home/local/PSYCH-ADS/xuqian_chen/Github/effort/1_code/test_function.ipynb')
data_folder_path <- file.path(dirname(script_dir), '0_data')
pipeline_folder_path <- file.path(dirname(script_dir), '2_pipeline/preprocessed')
external_path <- file.path(dirname(script_dir), '0_data/external')

# Load data
Rdfbias <- read.csv(file.path(pipeline_folder_path, 'foundations_R.csv'))
Ddfbias <- read.csv(file.path(pipeline_folder_path, 'foundations_D.csv'))
party_government_year <- read.csv(file.path(external_path, 'party_government_year.csv'))

dfbias <- merge(Rdfbias, Ddfbias, by = 'year', suffixes = c('_R', '_D'))
dfbias <- merge(dfbias, party_government_year[c('year', 'Presidency_party')], by = 'year', all.x = TRUE)

effort_R <- dfbias$effort_vir_vic_diff_R
effort_D <- dfbias$effort_vir_vic_diff_D

# Fit ARIMA models
model_R <- auto.arima(effort_R, seasonal = FALSE, stepwise = TRUE, trace = TRUE)
model_D <- auto.arima(effort_D, seasonal = FALSE, stepwise = TRUE, trace = TRUE)

# Extract residuals
residuals_R <- residuals(model_R)
residuals_D <- residuals(model_D)

# Compute Pearson correlation of residuals
corr <- cor(residuals_R, residuals_D)
p_value <- cor.test(residuals_R, residuals_D)$p.value
print(paste("Pearson correlation of residuals:", corr))
print(paste("P-value:", p_value))

# The differences in the results between Python and R could be due to several factors, including:

# Different underlying algorithms: Although both Python's pmdarima and R's forecast packages implement ARIMA modeling, there might be differences in the underlying algorithms or default settings, leading to slightly different results.

# Randomness: Some functions, such as auto.arima in R or auto_arima in Python, involve random processes (e.g., when searching for the best model). Running the functions multiple times might lead to slightly different results.

# Versions of libraries: Differences in the versions of libraries/packages used in Python and R can also lead to discrepancies in results.

# Floating-point arithmetic: Floating-point arithmetic can sometimes lead to small differences in numerical results between different programming languages or implementations.

# Given the nature of these factors, it's not uncommon to see slight differences in results between Python and R, even when using similar methods and datasets. However, in this case, the correlation values and p-values are quite close, indicating that both Python and R are capturing a similar relationship between the residuals of the ARIMA models for effort_R and effort_D.