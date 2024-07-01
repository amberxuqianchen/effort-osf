import pandas as pd
import os
import glob
# # Get the current script directory and create paths to the data and output folders
script_dir = os.path.dirname(os.path.abspath(__file__))
data_folder_path = os.path.join(script_dir, '..', '0_data/external')
preprocessed_folder_path = os.path.join(script_dir, '..', '2_pipeline/preprocessed')
out_folder_path = os.path.join(script_dir, '..', '2_pipeline/out')
tmp_folder_path = os.path.join(script_dir, '..', '2_pipeline/tmp')

# Load the csv file
df = pd.read_csv(os.path.join(data_folder_path,'gdp-per-capita-maddison-2020.csv'))

# Extract the rows for China and for years from 1950 onwards
gdp_df_chi = df[(df['Entity'] == 'China') & (df['Year'] >= 1950)]
gdp_df_us = df[(df['Entity'] == 'United States') & (df['Year'] >= 1873)]

# Prevalence data

prevalence_df = pd.read_csv(os.path.join(data_folder_path,'culturalvalues_EngAme.csv'))
# prevalence_df = pd.read_csv(os.path.join(preprocessed_folder_path,'COHA_list_frequencies_over_time.csv'))
if 'year' not in prevalence_df.columns:
    prevalence_df['year'] = prevalence_df['Year']
# drop rows if year < 1873 and rename Year to year
prevalence_df = prevalence_df[prevalence_df['year'] >= 1873]
prevalence_df_chi = pd.read_csv(os.path.join(data_folder_path,'prevalence_chi.csv'))

# Merge the two dataframes
# Assuming gdp_df and prevalence_df are your dataframes
external_df_chi = pd.merge(gdp_df_chi, prevalence_df, left_on='Year', right_on='year')
external_df = pd.merge(gdp_df_us, prevalence_df, left_on='Year', right_on='year')
# Columns to drop
columns_to_drop = ["Entity", "Code", "417485-annotations"]

# Drop the columns
external_df_chi = external_df_chi.drop(columns_to_drop, axis=1)
external_df = external_df.drop(columns_to_drop, axis=1)
# Save the China data to a new csv file
external_df_chi.to_csv(os.path.join(preprocessed_folder_path,'external_chi.csv') , index=False)
external_df.to_csv(os.path.join(preprocessed_folder_path,'external_us.csv') , index=False)

# read foundations df
foundations_df = pd.read_csv(os.path.join(preprocessed_folder_path,'foundations.csv'))
foundations_df_chi = pd.read_csv(os.path.join(preprocessed_folder_path,'foundations_chi.csv'))
# merge prevalence_df with foundations
dfus = pd.merge(external_df, foundations_df, on='year', how='outer')
dfchi = pd.merge(external_df_chi, foundations_df_chi, on='year', how='outer')

# save
dfus.to_csv(os.path.join(out_folder_path,'merged_us.csv') , index=False)
dfchi.to_csv(os.path.join(out_folder_path, 'merged_chi.csv') , index=False)

# # Sort the merged dataframe based on 'Year'
# merged_df = merged_df.sort_values('year')

# # Reset index after sorting
# merged_df.reset_index(drop=True, inplace=True)

# # delete % from column names for COHA
# merged_df.columns = merged_df.columns.str.replace('_%', '')
# # Write the merged dataframe to a new csv file
# # merged_df.to_csv(os.path.join(out_folder_path, 'merged_us.csv'), index=False)
# merged_df.to_csv(os.path.join(out_folder_path, 'merged_us_deletemissing.csv'), index=False)

