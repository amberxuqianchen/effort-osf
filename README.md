# effort-osf
Data and analysis scripts for project "Moral attitudes towards effort and efficiency:
A comparison between American and Chinese history"

# README: Moral Attitudes towards Effort and Efficiency

This project provides a historical analysis of the evolution of moral attitudes towards effort and efficiency in U.S. and Chinese contexts. It uses Natural Language Processing to study texts from U.S. Congressional Speeches and People's Daily of China.

## Getting Started

Before you can run the analysis, please ensure you have the following:

- Python 3.9
- Required Python packages: pandas, numpy, sklearn, matplotlib, seaborn
    - if you need to reproduce the word2vec model training: gensim, jieba, spacy, tqdm
- R and required packages for ARIMA and Granger analysis: forecast, tseries, lmtest, ggplot2

# Project Structure
## 0_data/
Contains all input data retrieved from external sources or word lists of dictionaries. The data in this folder remain identical to how they were retrieved or created.
  - `external/`: GDP, cultural values from Google Ngram Viewer, and the data of the U.S. congresses and party affiliation of presidents.
  - `wordlist/`: Dictionaries of words used in the analysis.


## 1_code/
Contains all code files for model training and analysis. The code files are named starting with a number to indicate the order of execution.

### Data Parsing and Training
- **01_congress_parse.ipynb**: Parse congressional speeches by year.
- **02_congress_training.py**: Train Word2Vec models based on the congressional speeches corpus by year.
- **03_PeopleDaily_training.py**: Train Word2Vec models based on People's Daily newspaper corpus by year.

### Word2Vec Calculation and Analysis
- **04_main.py**: Calculate cosine similarities between target concepts (effort and efficiency; also runs on the topic of USSR for validation) and moral foundations.
- **05_preprocessed_gdp_prevalence.py**: Preprocess the original GDP and cultural value prevalence data.
- **06_bcp_result_plot.R**: Apply Bayesian Change Point Detection on `2_pipeline/out/merged_us.csv` and `2_pipeline/out/merged_chi.csv`; results saved in `3_output/results/bcp/`. Also on validation data of USSR.
- **07_null_model.py**: Generate 10,000 pseudo dictionaries of moral foundations and rerun the processes of calculating cosine similarities between target concepts (effort and efficiency; USSR for validation) and pseudo moral foundations; generated pseudo dictionaries of random words are saved in `2_pipeline/tmp/null_association/` and the corresponding null data saved in `2_pipeline/tmp/`.
- **08_main_analysis_autoarima.r**: Apply ARIMA and Granger analysis on `2_pipeline/out/merged_us.csv` and `2_pipeline/out/merged_chi.csv`; results saved in `3_output/results/arima/` and `3_output/results/granger/`.
- **09_main_supp_plot.ipynb**: Generate all plots saved in `3_output/replication/plots/`.

### Supplementary Materials and Replication
- **10_supp_revision.ipynb**: Replicate the results for supplementary materials. To generate the necessary data:
  - **11_sentiment_analysis_congress.py**: Analyze the sentiment score of sentences with specified words from dictionaries.
  - **12_COHA_word_frequency.py**: Analyze cultural prevalence based on COHA.
  - **13_congress_parse_speeches_year_party_parallel.py**: Parse congressional speeches in parallel.
  - **14_congress_training_year_party.py**: Train Word2Vec models on congressional speeches organized by party affiliation and year.

### Further Analysis in Supplementary Material
- **15_revision_party_cor_of_arima_residual.r**: Analysis of ARIMA residuals by party correlation.
- **16_analysis_autoarima_COHA.r**: ARIMA analysis based on COHA data.
- **17_analysis_autoarima_deletemissing.r**: ARIMA analysis after handling missing data.
- **18_analysis_autoarima_sentiment.r**: ARIMA analysis based on sentiment data.

### Evaluation and Additional Calculations
- **19_difficulty_as_improvement.py**: Calculate the cosine similarity between target words and evaluation words preset in the dictionary.

### Function
- **extract_cosine_similarities.py**: Calculate the cosine similarity between different words in the Word2Vec models.

## 2_pipeline/
Organizes generated outputs.
  - `out/`: Final data for analysis.
  - `preprocessed/`: Preprocessed data to be merged.
  - `tmp/`: Temporary data for null model and validation.

## 3_output/ 
Contains final output files in the paper, including tables and figures.
  - `results/`: Stores results of ARIMA and Granger analysis.
    - `arima/`: ARIMA Models results (Table 1 and 2).
    - `granger/`: Granger test results (Table 3 and 4).
    - `bcp/`: results of Bayesian Change Point Detection.
  - `replication/plots`: All plots generated for the paper and supplementary materials.
  - `ussr/`: Stores data and results for USSR as validation.

# Reproduction

### Reproducing the Analysis

1. Clone this repository to your local machine.
2. Navigate to the `1_code` folder using the command line or terminal.
3. Run the `08_analysis_autoarima.R`. This script will generate the ARIMA Models results (Table 1 and 2) and Granger test results (Table 3 and 4), which will be saved in the `3_output/results/arima/` and `3_output/results/granger/` directories.
4. Run the `09_generate_plots.ipynb`. This script will generate all plots saved in `3_output/replication/plots/`.

### Reproducing the Word2Vec Model Training and Calculations of Word Similarities


- Run the `04_main.py` script. This script generates the data of cosine similarities between target concepts (i.e., effort and efficiency) and moral foundations showing the trend of moral values towards effort and efficiency over time for both the U.S. and China.
  - Trained Word2Vec models can be downloaded from [link]; note that you should change the paths of Word2Vec models to where you store the models on your local machine in the scripts if you intend to replicate the calculations of word similarities.


### Starting from Scratch

To start from scratch, follow the instructions contained within the script files:

- The raw texts of congressional speeches can be downloaded from [Stanford Congress Text Data](https://data.stanford.edu/congress_text).
- The raw texts of People's Daily newspaper are only available upon request (email amber.chen@psych.ucsb.edu).
- Run codes 01 ~03 to train the word2vec models.

## Contact
If you encounter any issues when trying to run this analysis, feel free to reach out at amber.chen@psych.ucsb.edu.

