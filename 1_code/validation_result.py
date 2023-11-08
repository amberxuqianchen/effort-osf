
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
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
# Set the global font to be Arial
mpl.rc('font', family='Arial')

# # Get the current script directory and create paths to the data and output folders
script_dir = os.path.dirname(os.getcwd())
data_folder_path = os.path.join(os.path.dirname(script_dir),'0_data')
pipeline_folder_path = os.path.join(os.path.dirname(script_dir),'2_pipeline/preprocessed')
tmp_folder_path =os.path.join(os.path.dirname(script_dir), '2_pipeline/tmp')
output_folder_path = os.path.join(os.path.dirname(script_dir), '3_output/ussr')
# Targets (e.g., age groups)
targets_path = os.path.join(data_folder_path, 'wordlist', 'dict_targets_USSR.json')
targets_chi_path = os.path.join(data_folder_path, 'wordlist', 'dict_targets_USSR_chi.json')
ussr = load_dict(targets_path)
ussr_chi = load_dict(targets_chi_path)

evaluations_set= {'foundations': foundations}
evaluations_chi_set = {'foundations_chi': foundations_chi}
ussr_similarity = calculate_cosine_similarities(models, ussr, foundations)
dfus = create_bias_dataframe(ussr_similarity, ussr, foundations)
ussr_chi_similarity = calculate_cosine_similarities(models_chi, ussr_chi, foundations_chi)
dfchi = create_bias_dataframe(ussr_chi_similarity, ussr_chi, foundations_chi)
dfus.to_csv(os.path.join(output_folder_path, 'dfus_ussr.csv'))
dfchi.to_csv(os.path.join(output_folder_path, 'dfchi_ussr.csv'))

# Filter dfus
dfus1920 = dfus[dfus['year'] >= 1920]

# Determine maximum absolute y-value for both datasets
max_abs_val_us = dfus1920['SovietUnion_vir_vic_diff'].abs().max()
# round to 3 decimal places
max_abs_val_us = round(max_abs_val_us, 1)
max_abs_val_chi = dfchi['SovietUnion_vir_vic_diff'].abs().max()

# Set Seaborn style and context for larger fonts and white background
sns.set(style="white", context="talk")

# Create a side-by-side plot
fig, axes = plt.subplots(1, 2, figsize=(18, 7))

# US data
axes[0].plot(dfus1920['year'], dfus1920['SovietUnion_vir_vic_diff'], lw=2, color='blue', label='USSR in US Congressional Speeches')
# axes[0].axhline(y=0, color='grey', linestyle='--')
axes[0].set_ylim([-max_abs_val_us, max_abs_val_us])

# Set the font size for event labels
event_label_font_size = 16

# Event Labels and Lines for the US
us_events = {
    1933: '1933 Diplomatic Ties',
    # 1945: '1945 The Gouzenko Affair',
    1949: '1949 First Atomic Bomb in USSR',
    1959: '1959 Khrushchev Visited US',
    # 1962: '1962 Cuban Missile Crisis'
}
y_position = max_abs_val_us - 0.04
for year, label in us_events.items():
    axes[0].text(year+1.2, y_position, label, verticalalignment='top',color='white',
                 fontsize=event_label_font_size,bbox=dict(facecolor='black', edgecolor='green', boxstyle='round,pad=0.5'))
    axes[0].axvline(x=year, ymin=-0.5, ymax=(y_position + max_abs_val_us) / (2 * max_abs_val_us), color='black', linestyle='--')
    y_position = y_position - 0.025
# y tick
axes[0].set_yticks([-0.1, -0.08, -0.06, -0.04, -0.02, 0, 0.02, 0.04, 0.06, 0.08, 0.1])
axes[0].legend(loc='upper left')
axes[0].set_xlabel('Year')
axes[0].set_ylabel('Embedding Bias (Virtue - Vice)')
axes[0].set_title('US')
sns.despine(ax=axes[0])
axes[0].text(-0.15, 1.05, 'A', transform=axes[0].transAxes, size=20, weight='bold')

# China data
axes[1].plot(dfchi['year'], dfchi['SovietUnion_vir_vic_diff'], lw=2, color='red', label='USSR in People’s Daily of China')
# axes[1].axhline(y=0, color='grey', linestyle='--')
axes[1].set_ylim([-max_abs_val_chi-0.1, max_abs_val_chi+0.1])
# Event Labels and Lines for China
china_events = {
    1960: '1960 Sino-Soviet Split',
    1969: '1969 Border Conflict',
    1991: '1991 Dissolution of the Soviet Union'
}
y_position = max_abs_val_chi - 0.025
for year, label in china_events.items():
    axes[1].text(year+0.9, y_position, label, verticalalignment='top',color='white',
                 fontsize=event_label_font_size,bbox=dict(facecolor='black', edgecolor='green', boxstyle='round,pad=0.5'))
    axes[1].axvline(x=year, ymin=-0.5, ymax=(y_position + max_abs_val_chi+0.05) / (2.5 * max_abs_val_chi), color='black', linestyle='--')
    y_position = y_position - 0.09

             
axes[1].legend(loc='upper left')
axes[1].set_xlabel('Year')
axes[1].set_ylabel('Embedding Bias (Virtue - Vice)')
axes[1].set_title('China')
sns.despine(ax=axes[1])
axes[1].text(-0.15, 1.05, 'B', transform=axes[1].transAxes, size=20, weight='bold')

plt.tight_layout()
# save the figure
plt.savefig(os.path.join(output_folder_path, 'ussr.png'), dpi=300)
plt.show()