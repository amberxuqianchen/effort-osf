from extract_cosine_similarities import load_dict, load_word2vec_models, calculate_cosine_similarities, create_bias_dataframe
import pandas as pd
import statistics
import random
import numpy as np
from gensim.models import KeyedVectors, Word2Vec
import os
import json
import nltk
import matplotlib.pyplot as plt
import seaborn as sns

# Download required NLTK data
nltk.download('words')
from nltk.corpus import words

# Define paths
script_dir = os.path.dirname(os.path.abspath('__file__'))
data_folder_path = os.path.join(os.path.dirname(script_dir), '0_data')
pipeline_folder_path = os.path.join(os.path.dirname(script_dir), '2_pipeline/preprocessed')
tmp_folder_path = os.path.join(os.path.dirname(script_dir), '2_pipeline/tmp')
null_folder_path = os.path.join(tmp_folder_path, 'null_association')
nullresults_folder_path = tmp_folder_path
# Evaluations
foundations_path = os.path.join(data_folder_path, 'wordlist', 'dict_foundations.json')
foundations_chi_path = os.path.join(data_folder_path, 'wordlist', 'dict_foundations_chi.json')

# Targets (e.g., age groups)
targets_path = os.path.join(data_folder_path, 'wordlist', 'dict_targets.json')
targets_chi_path = os.path.join(data_folder_path, 'wordlist', 'dict_targets_chi.json')

foundations = load_dict(foundations_path)
foundations_chi = load_dict(foundations_chi_path)
evaluations_set= {'foundations': foundations}
evaluations_chi_set = {'foundations_chi': foundations_chi}
targets = load_dict(targets_path)
targets_chi = load_dict(targets_chi_path)
# Models
model_chi_folder_path = '/home/local/PSYCH-ADS/xuqian_chen/Github/agebias-chi/0_data/model'
models_chi = load_word2vec_models(model_chi_folder_path)
model_folder_path = '/home/local/PSYCH-ADS/xuqian_chen/YES_lab/Amber/nlp/Congress/model'
models = load_word2vec_models(model_folder_path)

# Function to generate random words
def generate_random_words(evaluations, simnum, loadmodels, filename, checkwords=True):
    """
    Generate random words for null model
    
    Parameters:
    evaluations (dict): Dictionary of evaluations
    simnum (int): Number of simulations
    loadmodels (dict): Loaded word2vec models
    filename (str): Filename to save the null model
    checkwords (bool): Flag to check words against NLTK words corpus
    """
    null_filepath = os.path.join(null_folder_path, filename + 'null.json')
    if os.path.exists(null_filepath):
        with open(null_filepath, 'r') as f:
            null_lists = json.load(f)
    else:
        random.seed(1234)
        null_lists = []
        for _ in range(simnum):
            null_list = {}
            for evaluationname, evaluationwords in evaluations.items():
                if checkwords:
                    onelist = random.sample(words.words(), k=len(evaluationwords))
                else:
                    random_year = random.choice(list(loadmodels.keys()))
                    onelist = random.choices(list(loadmodels[random_year].wv.index_to_key), k=len(evaluationwords))
                null_list[evaluationname] = onelist
            null_lists.append(null_list)
        with open(null_filepath, 'w') as f:
            json.dump(null_lists, f)
    return null_lists

# Function to load null lists
def load_null_lists(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    else:
        raise FileNotFoundError("The specified file does not exist.")
# Function to calculate null association
def calculate_null_association(loadmodels, targets, evaluations, null_lists, savename):
    """
    Calculate null association using cosine similarities
    
    Parameters:
    loadmodels (dict): Loaded word2vec models
    targets (dict): Dictionary of targets
    evaluations (dict): Dictionary of evaluations
    null_lists (list): List of null word lists
    savename (str): Filename to save the results
    """
    null_similarities = []
    for null_list in null_lists:
        null_similarity = calculate_cosine_similarities(loadmodels, targets, null_list)
        dfnull = create_bias_dataframe(null_similarity, targets, evaluations)
        null_similarities.append(dfnull)
    dfnull_final = pd.concat(null_similarities)
    columns = ['year', 'effort_virtue', 'effort_vice', 'efficiency_virtue', 'efficiency_vice']
    dfnull_final = dfnull_final[columns]

    dfnull_final.to_csv(os.path.join(tmp_folder_path, savename + "_all.csv"))


    return dfnull_final

# Function to load null association
def load_null_association(savename):
    return pd.read_csv(os.path.join(nullresults_folder_path, savename + "_all.csv"))


# Generate or load null lists
null_lists = generate_random_words(foundations, 10000, models, 'foundation_word1000null',False)
# null_filepath = os.path.join(null_folder_path, 'foundation_word10000null.json')
# null_lists = load_null_lists(null_filepath)

# Calculate null associations for US data
dfnull_final = calculate_null_association(models, targets, foundations, null_lists, 'foundation10000_chinull')


# Culculate null associations for Chinese data
null_lists_chi = generate_random_words(foundations_chi, 10000, models_chi, 'foundation10000_chinull',False)
# null_filepath_chi = os.path.join(null_folder_path, 'foundation_chi_word10000null.json')
# null_lists_chi = load_null_lists(null_filepath_chi)
dfnull_final_chi = calculate_null_association(models_chi, targets_chi, foundations_chi, null_lists_chi, 'null10000_chi')