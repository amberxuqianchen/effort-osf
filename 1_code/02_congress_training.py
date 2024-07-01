import pandas as pd
import os
import sys
import gensim
from gensim.models import Word2Vec
import json

pro_dir = './Congress'
data_dir = "./Congress/hein-bound/"
text_dir = "./Congress/hein-bound_parsed/"
model_dir = "./Congress/model/"

# Read the congressyear.csv file into a dataframe
dfresults = pd.read_csv(os.path.join(pro_dir,'congressyear.csv'), dtype={'filenum': str} )

# Get the year value from the first command-line argument
# year = sys.argv[1]
for year in range(1874,2011):
	# Set the name of the output model file
	model_file = os.path.join(model_dir,str(year)+'.model')

	# Check if the model file already exists
	if not os.path.exists(model_file):
		# Filter the data in dfresults based on the specified year
		df_new = dfresults.loc[dfresults['year']==year]
		allline = []

		# Loop through each unique filenum in df_new
		for filenum in list(set(df_new['filenum'])):
			# Set the name of the input file
			infile = f'./Congress/hein-bound_parsed/speeches_{filenum}.jsonlist'

			# Open the input file and read the lines
			with open(infile, 'r') as f:
				lines = f.readlines()

				# Loop through the lines in the file
				for line in lines:
					# Load the JSON data from the line
					jline = json.loads(line)

					# Check if the speech_id is in df_new
					if int(jline['id']) in df_new['speech_id'].to_list():
						# Add the tokens from the line to allline
						allline.extend(jline['tokens'])

		# Set values for various parameters
		num_features = 100    # Word vector dimensionality
		min_word_count = 1    # Minimum word count
		num_workers = 31       # Number of threads to run in parallel
		context = 10          # Context window size
		downsampling = 1e-3   # Downsample setting for frequent words

		# Train the Word2Vec model on allline
		model_1 = Word2Vec(sentences = allline,
						sg=1,
						seed=1,
						min_count=min_word_count,
						window=context,
						sample=downsampling,
						workers=num_workers,
						size=num_features)

		# Save the model to the model_file
		model_1.save(model_file)

	else:
		print(str(model_file), "already exists")
