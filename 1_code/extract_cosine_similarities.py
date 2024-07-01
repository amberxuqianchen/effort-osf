import os
import json
import glob
from gensim.models import Word2Vec
import pandas as pd
import numpy as np

def load_dict(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        foundations = json.load(f)
    return foundations

def load_word2vec_models(model_folder_path: str):
    models = {}
    model_paths = glob.glob(os.path.join(model_folder_path, '*.model'))
    years = [int(path.split('.')[0][-4:]) for path in model_paths]

    # sort the years
    years.sort()
    for year in years:
        # get model path that contains the year
        model_path = [path for path in model_paths if str(year)+'.model' in path][0]
        
        models[year] = Word2Vec.load(model_path)
    return models

def load_word2vec_models_byparty(model_folder_path: str):
    
    Rmodels = {}
    Dmodels = {}
    model_paths = glob.glob(os.path.join(model_folder_path, '*.model'))
    # delete elements that contain 'npy
    model_paths = [path for path in model_paths if 'npy' not in path]
    years = [int(os.path.basename(path).split('.')[0].split('_')[0]) for path in model_paths]

    # sort the years
    years.sort()
    for year in years:
        # get model path that contains the year
        Rmodel_path = [path for path in model_paths if f'{year}_R.model' in path][0]
        Rmodels[year] = Word2Vec.load(Rmodel_path)

        # if [path for path in model_paths if f'{year}_D.model' in path] is not empty list:
        if any([f'{year}_D.model' in path for path in model_paths]):
            Dmodel_path = [path for path in model_paths if f'{year}_D.model' in path][0]
            Dmodels[year] = Word2Vec.load(Dmodel_path)
        else:
            print(f"Year {year} D model not found")
    return Rmodels,Dmodels

def calculate_cosine_similarities(models, targets, foundations):
    similarities = {}
    for year, model in models.items():
        similarities[year] = {}
        for target_name, target_words in targets.items():
            similarities[year][target_name] = {}
            for foundation_name, foundation_words in foundations.items():
                filtered_target_words = [word for word in target_words if word in model.wv.key_to_index]
                filtered_foundation_words = [word for word in foundation_words if word in model.wv.key_to_index]
                try:
                    similarity = model.wv.n_similarity(filtered_target_words, filtered_foundation_words)
                except:
                    similarity = np.nan
                    print(f'{year} {target_name} {foundation_name} Not found')

                similarities[year][target_name][foundation_name] = similarity
    return similarities

def calculate_cosine_similarities_synonyms(models, targets, foundations):
    similarities = {}
    for year, model in models.items():
        similarities[year] = {}
        for target_name, target_groups in targets.items():
            similarities[year][target_name] = {}
            for foundation_name, foundation_words in foundations.items():
                foundation_vecs = [word for word in foundation_words if word in model.wv.key_to_index]
                
                # Initialize list to store individual synonym group similarities
                group_similarities = []
                
                for target_group in target_groups:
                    # Filter target words to ensure they are in the model's vocabulary
                    target_vecs = [word for word in target_group if word in model.wv.key_to_index]
                    
                    # Calculate similarity for each synonym group
                    if target_vecs and foundation_vecs:  # Ensure both lists are not empty
                        try:
                            similarity = model.wv.n_similarity(target_vecs, foundation_vecs)
                            group_similarities.append(similarity)
                        except:
                            print(f'{year} {target_name} {foundation_name} Not found')
                    
                # Compute the average similarity for the target group if any similarities were calculated
                if group_similarities:
                    average_similarity = np.nanmean(group_similarities)
                else:
                    average_similarity = np.nan
                
                similarities[year][target_name][foundation_name] = average_similarity

    return similarities


def create_bias_dataframe(similarities: dict, targets: dict, foundations: dict) -> pd.DataFrame:
    colnames = ['year'] + [f'{target}_{foundation}' for foundation in foundations for target in targets]
    dfbias = pd.DataFrame(columns=colnames)
    for year, yearly_similarities in similarities.items():
        dfbias.loc[year] = [year] + [yearly_similarities[target][foundation] for col in colnames[1:] for target, foundation in [col.split('_', 1)]]
    if any("_" in key for key in list(foundations.keys())):

        for target in targets:
            for foundation in foundations:
                domain = foundation.split('_')[0]
                dfbias[f'{target}_{domain}'] = dfbias[f'{target}_{foundation}']
            dfbias[f'{target}_virtue'] = dfbias[[f'{target}_{foundation}' for foundation in foundations if 'vir' in foundation]].mean(axis=1)
            dfbias[f'{target}_vice'] = dfbias[[f'{target}_{foundation}' for foundation in foundations if 'vic' in foundation]].mean(axis=1)
            dfbias[f'{target}_vir_vic_diff'] = dfbias[f'{target}_virtue'] - dfbias[f'{target}_vice']
        return dfbias
    # dfbias.set_index('year', inplace=True)
    else:
        return dfbias
