
import os
import pandas as pd
from extract_cosine_similarities import load_dict , load_word2vec_models, calculate_cosine_similarities,create_bias_dataframe

# # Get the current script directory and create paths to the data and output folders
script_dir = os.path.dirname(os.path.abspath(__file__))
data_folder_path = os.path.join(os.path.dirname(script_dir),'0_data')
pipeline_folder_path = os.path.join(os.path.dirname(script_dir),'2_pipeline/preprocessed')
tmp_folder_path =os.path.join(os.path.dirname(script_dir), '2_pipeline/tmp')

# Evaluations
foundations_path = os.path.join(data_folder_path, 'wordlist', 'dict_foundations.json')
foundations_chi_path = os.path.join(data_folder_path, 'wordlist', 'dict_foundations_chi.json')

# Targets (e.g., age groups)
targets_path = os.path.join(data_folder_path, 'wordlist', 'dict_targets.json')
targets_chi_path = os.path.join(data_folder_path, 'wordlist', 'dict_targets_chi.json')

foundations = load_dict(foundations_path)
foundations_chi = load_dict(foundations_chi_path)

targets = load_dict(targets_path)
targets_chi = load_dict(targets_chi_path)

# Models
# model_folder_path = os.path.join(data_folder_path, 'model')
model_folder_path = '/home/local/PSYCH-ADS/xuqian_chen/YES_lab/Amber/nlp/Congress/model'
model_chi_folder_path = '/home/local/PSYCH-ADS/xuqian_chen/Github/agebias-chi/0_data/model'

# models = load_word2vec_models(model_folder_path)
models_chi = load_word2vec_models(model_chi_folder_path)

# Change or add foundations to the dictionary here as needed
# For example:
# foundations['new_foundation_name'] = ['word1', 'word2', 'word3']

evaluations_set= {'foundations': foundations}
evaluations_chi_set = {'foundations_chi': foundations_chi}

for name, evaluations in evaluations_set.items():
    # Calculate cosine similarities
    similarities = calculate_cosine_similarities(models, targets, evaluations)

    # Calculate embedding bias
    dfbias = create_bias_dataframe(similarities, targets, evaluations)
    
    # Save the DataFrame as a CSV
    csv_filepath = os.path.join(pipeline_folder_path, name+ '.csv')
    dfbias.to_csv(csv_filepath, index=False)
    print('finish English')
    
for name, evaluations in evaluations_chi_set.items():
    # Calculate cosine similarities
    similarities = calculate_cosine_similarities(models_chi, targets_chi, evaluations)

    # Calculate embedding bias
    dfbias = create_bias_dataframe(similarities, targets_chi, evaluations)
    
    # Save the DataFrame as a CSV
    csv_filepath = os.path.join(pipeline_folder_path, name+ '.csv')
    dfbias.to_csv(csv_filepath, index=False)
    print('finish Chinese')

# # Validation: USSR
# # Targets
targets_path = os.path.join(data_folder_path, 'wordlist', 'dict_targets_USSR.json')
targets_chi_path = os.path.join(data_folder_path, 'wordlist', 'dict_targets_USSR_chi.json')
ussr = load_dict(targets_path)
ussr_chi = load_dict(targets_chi_path)

ussr_similarity = calculate_cosine_similarities(models, ussr, foundations)
dfus = create_bias_dataframe(ussr_similarity, ussr, foundations)
ussr_chi_similarity = calculate_cosine_similarities(models_chi, ussr_chi, foundations_chi)
dfchi = create_bias_dataframe(ussr_chi_similarity, ussr_chi, foundations_chi)

dfus.to_csv(os.path.join(tmp_folder_path, 'dfus_ussr.csv'))
dfchi.to_csv(os.path.join(tmp_folder_path, 'dfchi_ussr.csv'))