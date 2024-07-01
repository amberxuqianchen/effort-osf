import os
import json
import pandas as pd
from gensim.models import Word2Vec
from concurrent.futures import ProcessPoolExecutor
import re
mainpath = '/home/local/PSYCH-ADS/xuqian_chen/YES_lab/Amber/nlp'
# Define directories
pro_dir = '../2_pipeline/preprocessed/'
mainpath = '/home/local/PSYCH-ADS/xuqian_chen/YES_lab/Amber/nlp'
data_dir = mainpath + "/Congress/hein-bound/"
text_dir = mainpath + "/Congress/hein-bound_parsed_party_year/"
model_dir = mainpath + "/Congress/model_by_year_party/"
clean_text_folder = os.path.join(mainpath, 'hein-bound_cleaned_party_year')

# Ensure dirs exist
if not os.path.exists(model_dir):
    os.makedirs(model_dir)

if not os.path.exists(clean_text_folder):
    os.makedirs(clean_text_folder)

# Read the congressyear.csv into a dataframe
dfresults = pd.read_csv(os.path.join(pro_dir, 'congress_party_year.csv'), dtype={'filenum': str})

def clean_text(text):
	# Remove any non-alphanumeric characters
	text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
	# Convert to lowercase
	text = text.lower()
	# remove digitsπ
	text = re.sub(r'\d+', '', text)

	return text

def train_model_for_year_party(year, party, dfresults):
	model_file = os.path.join(model_dir, f'{year}_{party}.model')
	if not os.path.exists(model_file):
		print(f"Training model for year {year}, party {party}")
		df_new = dfresults[(dfresults['year'] == year) & (dfresults['party_code'] == party)]

		allline = []
		
		for filenum in df_new['filenum'].unique():
			filenum = str(filenum).zfill(3)
			infile = os.path.join(text_dir, f'speeches_{filenum}_{year}_{party}.json')

			if os.path.exists(infile):
				with open(infile, 'r') as f:
					for line in f:
						if line.strip():  # Check if the line is not empty
							try:
								jline = json.loads(line)
								# Clean each token in each sentence
								for sentence in jline['tokens']:  
									clean_sentence = [clean_text(token) for token in sentence]
									# Remove any empty tokens
									clean_sentence = [token for token in clean_sentence if token]
									allline.append(clean_sentence)
							except json.JSONDecodeError as e:
								print(f"Error decoding JSON: {e}")
								print(f"Skipping line: {line}")
	
		if allline:
			# save the list of sentences of tokens to a json file
			outfile = os.path.join(clean_text_folder, f'{year}_{party}_cleaned.json')
			with open(outfile, 'w') as f:
				json.dump(allline, f)
			num_allline = len(allline)
			print(f"{num_allline} sentences of tokens saved to {outfile}")
			model = Word2Vec(sentences=allline)

			model.save(model_file)
			print(f"Model saved for year {year}, party {party} at {model_file}")
		else:
			print(f"No data to train the model for year {year}, party {party}.")
	else:
		print(f"Model already exists for year {year}, party {party} at {model_file}")


with ProcessPoolExecutor(max_workers=os.cpu_count() - 1) as executor:
	futures = []
	years = range(1939,1941)
	# for year in dfresults['year'].unique():
	for year in years:
		for party in ['D', 'R']:  # Assuming parties are 'D' (Democrat) and 'R' (Republican)
			if (dfresults['party_code'] == party).any():
				futures.append(executor.submit(train_model_for_year_party, year, party, dfresults))

	for future in futures:
		future.result()  # This blocks until the future is complete


