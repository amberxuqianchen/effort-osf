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
# drop rows if year < 1873 and rename Year to year
prevalence_df = prevalence_df[prevalence_df['year'] >= 1873]
prevalence_df_chi = pd.read_csv(os.path.join(data_folder_path,'prevalence_chi.csv'))

# Merge the two dataframes
# Assuming gdp_df and prevalence_df are your dataframes
external_df_chi = pd.merge(gdp_df_chi, prevalence_df, left_on='Year', right_on='year')
external_df = pd.merge(gdp_df_us, prevalence_df, left_on='Year', right_on='year')
# Columns to drop
columns_to_drop = ["Entity", "Code", "417485-annotations", "Year"]

# Drop the columns
external_df_chi = external_df_chi.drop(columns_to_drop, axis=1)
external_df = external_df.drop(columns_to_drop, axis=1)
# Save the China data to a new csv file
external_df_chi.to_csv(os.path.join(preprocessed_folder_path,'external_chi.csv') , index=False)
external_df.to_csv(os.path.join(preprocessed_folder_path,'external_us.csv') , index=False)
csv_files = glob.glob(os.path.join(preprocessed_folder_path, '*.csv'))
csv_files_chi = [x for x in csv_files if 'chi' in x]
csv_files_us = [x for x in csv_files if 'chi' not in x]

# Create an empty list to store dataframes
dfs = []

# Read and append each csv file into the list
for csv_file in csv_files_chi:
    df = pd.read_csv(csv_file)
    df['year'] = df['year'].astype(int)
    dfs.append(df)

# Merge DataFrames
merged_df = dfs[0]
for df in dfs[1:]:
    merged_df = pd.merge(merged_df, df, on='year', how='outer')

# Sort the merged dataframe based on 'Year'
merged_df = merged_df.sort_values('year')

# Reset index after sorting
merged_df.reset_index(drop=True, inplace=True)

# Write the merged dataframe to a new csv file
merged_df.to_csv(os.path.join(out_folder_path, 'merged_chi.csv'), index=False)

# Create an empty list to store dataframes
dfs = []

# Read and append each csv file into the list
for csv_file in csv_files_us:
    df = pd.read_csv(csv_file)
    df['year'] = df['year'].astype(int)
    # replace efficienci with efficiency in column names
    df.columns = df.columns.str.replace('efficienci', 'efficiency')
    dfs.append(df) 

# Merge DataFrames
merged_df = dfs[0]
for df in dfs[1:]:
    merged_df = pd.merge(merged_df, df, on='year', how='outer')

# Sort the merged dataframe based on 'Year'
merged_df = merged_df.sort_values('year')

# Reset index after sorting
merged_df.reset_index(drop=True, inplace=True)

# Write the merged dataframe to a new csv file
merged_df.to_csv(os.path.join(out_folder_path, 'merged_us.csv'), index=False)

