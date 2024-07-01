from extract_cosine_similarities import load_dict, load_word2vec_models, calculate_cosine_similarities, create_bias_dataframe
import pandas as pd
import statistics
import random
import numpy as np
from gensim.models import KeyedVectors
from gensim.models import Word2Vec
import os
import json
import nltk
# nltk.download('words')
from nltk.corpus import words
# # Get the current script directory and create paths to the data and output folders
script_dir = os.path.dirname('/home/local/PSYCH-ADS/xuqian_chen/Github/effort/1_code/test_function.ipynb')
data_folder_path = os.path.join(os.path.dirname(script_dir),'0_data')
pipeline_folder_path = os.path.join(os.path.dirname(script_dir),'2_pipeline/preprocessed')
tmp_folder_path =os.path.join(os.path.dirname(script_dir), '2_pipeline/tmp')
# Models
model_folder_path = '/home/local/PSYCH-ADS/xuqian_chen/YES_lab/Amber/nlp/Congress/model'
models = load_word2vec_models(model_folder_path)

# Targets
dict_path = os.path.join(data_folder_path, 'wordlist', 'dict_difficulty_improvement.json')
dict = load_dict(dict_path)

evaluations_set= {'Improvement': dict['Improvement'],'Impossibility': dict['Impossibility'],"Importance": dict['Importance']}
targets_set = {'Difficulty':dict['Difficulty']}

diff_improve_similarity = calculate_cosine_similarities(models,targets_set, evaluations_set)
dfus = create_bias_dataframe(diff_improve_similarity,targets_set, evaluations_set)
# save the dataframe to preprocessed folder
dfus.to_csv(os.path.join(pipeline_folder_path, 'bias_difficulty_improvement.csv'), index=False)
