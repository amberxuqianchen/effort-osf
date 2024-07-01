import pickle
import os
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import string
import json

# Setup paths
parse_dir = '/home/local/PSYCH-ADS/xuqian_chen/YES_lab/Amber/nlp/COHA/parsed_tokens/'
file_dir = os.path.dirname(os.path.abspath(__file__))
dict_dir = os.path.join(file_dir, '../0_data/wordlist/')
preprocessed_dir = os.path.join(file_dir, '../2_pipeline/preprocessed/')
output_plot_dir = os.path.join(file_dir, '../3_output/plot/COHA_word_frequency/')

# Load the word lists as dictionaries from JSON
dict_file_path = os.path.join(dict_dir, 'dict_culture.json')
with open(dict_file_path, 'r') as f:
    word_lists= json.load(f)

years = range(1873, 2012)  # Specify the range of years

# Initialize a DataFrame to store results for list percentages and individual word counts
columns = ['Year'] + [f'{list_name}_%' for list_name in word_lists.keys()]
results_df = pd.DataFrame(columns=columns)

# Function to clean and preprocess tokens
def clean_tokens(tokens):
    return [token.lower() for token in tokens if token.isalpha() and token not in string.punctuation]

# Store individual word frequencies in a separate DataFrame
word_details_columns = ['Year', 'Word', 'Frequency', 'Percentage']
word_details_df = pd.DataFrame(columns=word_details_columns)

# Process each year
for year in years:
    token_file = os.path.join(parse_dir, f'all_{year}.pkl')
    try:
        with open(token_file, "rb") as f:
            sents = pickle.load(f)
    except FileNotFoundError:
        print(f"Token file for year {year} not found. Skipping.")
        continue
    
    # Flatten the list of sentences to a list of words and clean them
    words = clean_tokens([word for sent in sents for word in sent])
    
    # Calculate word frequencies
    word_freq = Counter(words)
    total_words = sum(word_freq.values())
    
    # Calculate frequencies and percentages for each word list
    data = {'Year': year}
    for list_name, word_list in word_lists.items():
        list_count = sum(word_freq[word] for word in word_list)
        list_percentage = (list_count / total_words) * 100 if total_words > 0 else 0
        data[f'{list_name}_%'] = list_percentage
        
        # Save individual word frequencies
        for word in word_list:
            word_count = word_freq[word]
            word_percentage = (word_count / total_words) * 100 if total_words > 0 else 0
            new_row = pd.DataFrame({'Year': [year], 'Word': [word], 'Frequency': [word_count], 'Percentage': [word_percentage]})
            word_details_df = pd.concat([word_details_df, new_row], ignore_index=True)

    
    # Append the results to the DataFrame use concat
    results_df = pd.concat([results_df, pd.DataFrame(data, index=[0])], ignore_index=True)

# Save results to CSV
results_df.to_csv(preprocessed_dir + 'COHA_list_frequencies_over_time.csv', index=False)
word_details_df.to_csv(preprocessed_dir + 'COHA_individual_word_frequencies.csv', index=False)

# Visualization (only for word lists)
plt.figure(figsize=(12, 8))
for column in columns[1:]:  # Skip the 'Year' column
    plt.plot(results_df['Year'], results_df[column], label=column)

plt.title('Word List Frequency Percentage Over Time')
plt.xlabel('Year')
plt.ylabel('Frequency Percentage (%)')
plt.legend(title='Word Lists')
plt.grid(True)
# Save the plot
plt.savefig(output_plot_dir + 'COHA_word_frequency.png', dpi=300, format='png')  
plt.show()
