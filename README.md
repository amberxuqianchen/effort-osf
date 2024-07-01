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

## Project Structure

- `0_data/`: Contains all input data retrieved from external sources or word lists of dictionaries. The data in this folder remain identical to how they were retrieved or created.
  - `external/`: GDP, cultural values from Google Ngram Viewer, and the data of the U.S. congresses and party affiliation of presidents.
  - `wordlist/`: Dictionaries of words used in the analysis.

- `1_code/`: Contains all code files for model training and analysis. The code files are named starting with a number to indicate the order of execution.
  - `01_congress_parse.ipynb`: Parse congressional speeches by year.
  - `02_congress_training.py`: Train Word2Vec models based on the congressional speeches corpus by year.
  - `03_PeopleDaily_training.py`: Train Word2Vec models based on People's Daily newspaper corpus by year.
  - `04_extract_cosine_similarities.py`: Calculate the cosine similarity between different words in the Word2Vec models.
  - `05_main.py`: Calculate cosine similarities between target concepts (effort and efficiency; ussr for validation) and moral foundations.
  - `06_preprocessed_gdp_prevalence.py`: Preprocess the original GDP and cultural value prevalence data.
 
  - `07_bcp_result_plot.R.r`: Apply Bayesian Change Point Detection on `2_pipeline/out/merged_us.csv` and `2_pipeline/out/merged_chi.csv`; results saved in `3_output/results/bcp/`.
  - `08_main_analysis_autoarima.r`: Apply ARIMA and Granger analysis on `2_pipeline/out/merged_us.csv` and `2_pipeline/out/merged_chi.csv`; results saved in `3_output/results/arima/` and `3_output/results/granger/`.
  - `09_main_supp_plot.ipynb`: Generate all plots saved in `3_output/replication/plots/`.
  - `10_sentiment_analysis_congress.py`: Analyze the sentiment score of sentences with specified words from dictionaries.
  - `11_COHA_word_frequency.py`: Analyze cultural prevalence based on COHA.
  - `12_congress_parse_speeches_year_party_parallel.py`: Parse congressional speeches in parallel.
  - `13_congress_training_year_party.py`: Train Word2Vec models on congressional speeches organized by party affiliation and year.
  
  - `15_revision_party_cor_of_arima_residual.r`: Parse congressional speeches in parallel.
  
  - `16_difficulty_as_improvement.py`: Calculate the cosine similarity between target words and evaluation words preset in the dictionary.

- `2_pipeline/`: Organizes generated outputs.
  - `out/`: Final data for analysis.
  - `preprocessed/`: Preprocessed data to be merged.
  - `tmp/`: Temporary files (can be deleted).

- `3_output/`: Contains final output files in the paper, including tables and figures.
  - `results/`: Stores results of ARIMA and Granger analysis.
    - `arima/`: ARIMA Models results (Table 1 and 2).
    - `granger/`: Granger test results (Table 3 and 4).
  - `replication/`: Stores replication materials.
    - `plots/`: All plots generated for the paper and supplementary materials.


- 0_data: contains all input data retrieved from external sources or word lists of dictionaries. The data in this folder remain identical to the way it was retrieved or created.
- 1_code: contains all code files for model training and analysis. The code files are named starting with a number to indicate the order of execution.
- 2_pipeline: contains three sub-folders: out (final data for analysis), preprocessed (preprocessed data to be merged), and tmp (can be deleted), to organize generated outputs.
- 3_output: contains final output files in the paper, including tables and figures.

## Reproduction

### Reproducing the Analysis

1. Clone this repository to your local machine.
2. Navigate to the `1_code` folder using the command line or terminal.
3. Run the `main.py` script with the command `python main.py`. This script generates the data of consine similarities between target concepts (i.e., effort and efficiency) and moral foundations showing the trend of moral values towards effort and efficiency over time for both the U.S. and China.
4. Run the `main_analysis_autoarima.r`. This script will generate the ARIMA Models results (Table 1 and 2) and Granger test results (Table 3 and 4), which will be saved in the `3_output/results/arima/` and  `3_output/results/granger/` directories.
5. Run the `main_supp_plot.ipynb`. This script will generate all plots saved in `3_output/replication/plots/`.

### Reproducing the Analysis
Note that the raw texts of congressional speeches can be downlowded from [https://data.stanford.edu/congress_text]; the raw texts of People's Daily newspaper is only available upon request (email amber.chen@psych.ucsb.edu).



### Functions of code files

| Filename | Function |
| --- | --- |
| congress_parse.ipynb | Parse congressional speeches by year. |
| congress_training.py | Training word2vec models based on congressional speeches corpus by year. |
| PeopleDaily_training.py | Training word2vec models based on People's Daily newspaper corpus by year. |
| extract_cosine_similarities.py | Function of calculating the cosine similarity between different words in the word2vec models. |
| main.py | Execution of Calculating the cosine similarity between different words in the word2vec model. |
| preprocessed_gdp_prevalence.py | Preprocess the original GDP and cultural value prevalence data. |
| merge_preprocessed.py | Merge all CSV files (moral values, GDP, and cultural values) into one and perform related sorting and reset indexing. |
| main_analysis_autoarima.r | Reproduce main results of table 1-4: applied ARIMA and Granger analysis on `2_pipeline/out/merged_us.csv` and `2_pipeline/out/merged_chi.csv`; results saved in `3_output/results/arima/` and `3_output/results/granger/`. |
| main_supp_plot.ipynb | Reproduce all plots in the paper and supplementary materials; all plots saved in `3_output/replication/plots/`. |
| sentiment_analysis_congress.py | Analyze the sentiment score of sentences with specified words from dictionaries. |
| COHA_word_frequency.py | Cultural prevalence based on COHA. |
| main.py | Perform sentiment analysis on the text vector model and save the processing results as a CSV file. |
| congress_training_year_party.py | Perform word vector training on Congressional speeches organized by party affiliation and year. |
| main_plot.py | Visually process the analysis results of text data. |
| congress_parse_speeches_year_party_parallel.py | Parse Congressional speeches in parallel. |
| difficulty_as_improvement.py | Calculate the cosine similarity between the target words and evaluation words preset in the dictionary. |

## Contact

If you encounter any issues when trying to run this analysis, feel free to reach out.

