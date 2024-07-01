import os
import pandas as pd
from extract_cosine_similarities import load_dict , load_word2vec_models, calculate_cosine_similarities, create_bias_dataframe
# script_dir = os.path.dirname(os.path.abspath(__file__))
script_dir = os.path.dirname(os.path.abspath('__file__'))
data_folder_path = os.path.join(script_dir, '..', '0_data')
pipeline_folder_path = os.path.join(script_dir, '..', '2_pipeline/preprocessed')
tmp_folder_path = os.path.join(script_dir, '..', '2_pipeline/tmp')

# Targets (e.g., age groups)
targets_path = os.path.join(data_folder_path, 'wordlist', 'dict_targets.json')
targets_chi_path = os.path.join(data_folder_path, 'wordlist', 'dict_targets_chi.json')

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


import os
import matplotlib.pyplot as plt
import numpy as np
from nltk.sentiment import SentimentIntensityAnalyzer
from collections import defaultdict
from tqdm import tqdm
import nltk
nltk.download('vader_lexicon')
# Initialize VADER
sia = SentimentIntensityAnalyzer()

def read_files_and_extract_sentences(start_year, end_year, keywords):
    path = '/home/local/PSYCH-ADS/xuqian_chen/YES_lab/Amber/nlp/Congress/hein-bound_parsed'  # Adjust to your files' path
    relevant_sentences = defaultdict(list)
    for year in tqdm(range(start_year, end_year + 1)):
        filename = os.path.join(path, f'cleaned_tokens_{year}.txt')
        try:
            with open(filename, 'r') as file:
                for line in file:
                    if any(word in line for word in keywords):
                        relevant_sentences[year].append(line.strip())
        except FileNotFoundError:
            print(f"File not found: {filename}")
    return relevant_sentences


def calculate_sentiments(sentences):
    sentiment_scores = {'pos': [], 'neg': [], 'neu': [], 'compound': []}
    for sentence in sentences:
        scores = sia.polarity_scores(sentence)
        sentiment_scores['pos'].append(scores['pos'])
        sentiment_scores['neg'].append(scores['neg'])
        sentiment_scores['neu'].append(scores['neu'])
        sentiment_scores['compound'].append(scores['compound'])
    return sentiment_scores


# Extract sentences
sentences_effort = read_files_and_extract_sentences(1873, 2011, targets['effort'])
sentences_efficiency = read_files_and_extract_sentences(1873, 2011, targets['efficiency'])

# Calculate sentiments with tqdm
sentiments_effort = {year: calculate_sentiments(sentences) for year, sentences in tqdm(sentences_effort.items())}
sentiments_efficiency = {year: calculate_sentiments(sentences) for year, sentences in tqdm(sentences_efficiency.items())}

# save to pipeline folder
df_effort = pd.DataFrame(sentiments_effort)
df_efficiency = pd.DataFrame(sentiments_efficiency)
df_effort.to_csv(os.path.join(pipeline_folder_path, 'sentiments_effort_raw.csv'))
df_efficiency.to_csv(os.path.join(pipeline_folder_path, 'sentiments_efficiency_raw.csv'))
