import os
import json
import pandas as pd
from tqdm import tqdm
import spacy
from concurrent.futures import ProcessPoolExecutor, as_completed

def process_congress_speeches(group, indir, outdir, encoding, nlp):
    outlines = {}
    congress_num = str(group['filenum'].values[0]).zfill(3)
    speech_file_path = os.path.join(indir, group['speech_file'].iloc[0])
    print(f"Processing {speech_file_path}")
    for year in group['year'].unique():
        for party in group['party_code'].unique():
            speech_year_party_name = f'speeches_{congress_num}_{year}_{party}'
            if not os.path.exists(os.path.join(outdir, f'{speech_year_party_name}.json')):
                print(f"Processing year {year} and party {party}")
                speech_id_expected = group[(group['year'] == year) & (group['party_code'] == party)]['speech_id']
                speech_id_expected = speech_id_expected.astype(int).tolist()
                
                with open(speech_file_path, encoding=encoding) as f:
                    outlines_by_speech_id = {}
                    for line in f:
                        line = line.strip()
                        parts = line.split('|')
                        speech_id = parts[0]
                        if speech_id != 'speech_id' and int(speech_id) in speech_id_expected:
                            text = parts[1] if len(parts) > 1 else ""
                            parsed = nlp(text)
                            sents = [sent.text for sent in parsed.sents]
                            tokens = [[token.text for token in sent] for sent in parsed.sents]
                            outlines_by_speech_id[speech_id] = {'id': speech_id, 'sents': sents, 'tokens': tokens}

                
                outfile_json = os.path.join(outdir, f'{speech_year_party_name}.json')
                print(f"Saving {len(outlines_by_speech_id)} entries to {outfile_json}")
                with open(outfile_json, 'w') as fo_json:
                    for speech_id, data in outlines_by_speech_id.items():
                        fo_json.write(json.dumps(data) + '\n')
            else:
                print(f"File {speech_year_party_name} exists, skipping...")
    
    return f"Completed processing for {congress_num}"

# Load data and initialize settings
mainpath = '/home/local/PSYCH-ADS/xuqian_chen/YES_lab/Amber/nlp'
indir = os.path.join(mainpath, 'Congress/hein-bound/')
outdir = os.path.join(mainpath, 'Congress/hein-bound_parsed_party_year/')
encoding = 'Windows-1252'
nlp = spacy.load("en_core_web_sm")

df = pd.read_csv(os.path.join(mainpath, 'Congress/congress_party_year.csv'))
df = df[df['party_code'].isin(['D', 'R'])]
def run_processing(df, indir, outdir, encoding):
    # Get the number of available CPU cores and leave one unoccupied
    num_cores = max(1, os.cpu_count() - 1)
    with ProcessPoolExecutor(max_workers=num_cores) as executor:
        futures = {executor.submit(process_congress_speeches, df[df['filenum'] == congress], indir, outdir, encoding, nlp): congress for congress in df['filenum'].unique()}
        for future in as_completed(futures):
            print(future.result())

# Example call to process in parallel
run_processing(df, indir, outdir, encoding)
