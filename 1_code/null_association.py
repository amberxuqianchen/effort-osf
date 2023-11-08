import os
import pandas as pd
from extract_cosine_similarities import load_dict , load_word2vec_models, calculate_cosine_similarities,create_bias_dataframe

# # Get the current script directory and create paths to the data and output folders
script_dir = os.path.dirname(os.path.abspath(__file__))
data_folder_path = os.path.join(os.path.dirname(script_dir),'0_data')
pipeline_folder_path = os.path.join(os.path.dirname(script_dir),'2_pipeline/preprocessed')
tmp_folder_path =os.path.join(os.path.dirname(script_dir), '2_pipeline/tmp')
null_folder_path = os.path.join(tmp_folder_path, 'null_association')

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

# Change or add foundations to the dictionary here as needed
# For example:
# foundations['new_foundation_name'] = ['word1', 'word2', 'word3']

evaluations_set= {'foundations': foundations}
evaluations_chi_set = {'foundations_chi': foundations_chi}

import statistics
import random
import numpy as np
from gensim.models import KeyedVectors
from gensim.models import Word2Vec
import json
import nltk
nltk.download('words')
from nltk.corpus import words
import matplotlib.pyplot as plt
import seaborn as sns

nullresults_folder_path =os.path.join(os.path.dirname(script_dir),'2_pipeline/tmp')
nullplot_folder_path = os.path.join(os.path.dirname(script_dir),'3_output', 'plot','null_association')
if not os.path.exists(nullplot_folder_path):
    os.makedirs(nullplot_folder_path)

def generate_random_words(evaluations, simnum, loadmodels, tmp_folder_path, filename,checkwords=True):
    """Parameters:
    length: the number of words in the list of domains (e.g., moral foundation, agiest attitude, etc.)
    """
    null_filepath = os.path.join(null_folder_path, filename + 'null.json')
    if os.path.exists(null_filepath):
        with open(null_filepath, 'r') as f:
            null_lists = json.load(f)
    else:
        # set seed
        random.seed(1234)
        # generate random words
        null_lists = []
        for _ in range(simnum):
            null_list = {}
            for evaluationname,evaluationwords in evaluations.items():
            # get random words from the true word vocabulary, the length is the same as the target
                if checkwords:
                    onelist = random.sample(words.words(),k=len(evaluationwords))
                else:
                    random_year = random.choice(list(loadmodels.keys()))
                    onelist = random.choices(list(loadmodels[random_year].wv.index_to_key),k=len(evaluationwords))
                null_list[evaluationname] = onelist
            null_lists.append(null_list)
 
        # save the null list
        with open(null_filepath, 'w') as f:
            json.dump(null_lists, f)
            print(f'null list saved: {null_filepath}')
    return null_lists

def calculate_null_association(loadmodels, targets, evaluations, null_lists,savename):
    """Parameters:
    loadmodels: a dictionary of models
    targets: a dictionary of targets
    evaluations: a dictionary of evaluations
    null_lists: a list of null lists
    """
    # calculate cosine similarities
    null_similarities = []
    for null_list in null_lists:
        null_similarity = calculate_cosine_similarities(loadmodels, targets, null_list)
        dfnull = create_bias_dataframe(null_similarity, targets, evaluations)
        null_similarities.append(dfnull)
    # put all null similarities together
    dfnull_final = pd.concat(null_similarities)

    columns = ['year', 'effort_virtue','effort_vice','efficiency_virtue','efficiency_vice']
    dfnull_final = dfnull_final[columns]
    
    # Saving the results
    dfnull_final.to_csv(os.path.join(tmp_folder_path, savename + "_all.csv"))

    return dfnull_final
