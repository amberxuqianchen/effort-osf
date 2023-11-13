from null_association import *
import matplotlib.pyplot as plt
import seaborn as sns
script_dir = os.path.dirname(os.path.abspath(__file__))
data_folder_path = os.path.join(os.path.dirname(script_dir),'0_data')
pipeline_folder_path = os.path.join(os.path.dirname(script_dir),'2_pipeline/preprocessed')
tmp_folder_path =os.path.join(os.path.dirname(script_dir), '2_pipeline/tmp')
bcp_null_path = os.path.join(os.path.dirname(script_dir),'3_output', 'plot')
nullresults_folder_path =os.path.join(os.path.dirname(script_dir),'2_pipeline/tmp')

null_folder_path = os.path.join(tmp_folder_path, 'null_association')
# nullresults_folder_path = os.path.join(os.path.dirname(script_dir),'3_output', 'results','null_association')
nullplot_folder_path = os.path.join(os.path.dirname(script_dir),'3_output', 'plot','null_association')
if not os.path.exists(null_folder_path):
    os.makedirs(null_folder_path)
if not os.path.exists(nullresults_folder_path):
    os.makedirs(nullresults_folder_path)
if not os.path.exists(nullplot_folder_path):
    os.makedirs(nullplot_folder_path)
if not os.path.exists(tmp_folder_path):
    os.makedirs(tmp_folder_path)
# load nulldata
def load_null_association(savename):
    dfnull_final = pd.read_csv(os.path.join(nullresults_folder_path, savename + "_all.csv"))
    return dfnull_final
# US Congress
us_null_filepath = os.path.join(nullresults_folder_path, 'us_trueword10000_all.csv"')
# if os.path.exists(us_null_filepath):
dfusnull_final = pd.read_csv(os.path.join(nullresults_folder_path,'us_trueword10000_all.csv'))
# else:
#     # Models
#     # model_folder_path = os.path.join(data_folder_path, 'model')
# model_folder_path = '/home/local/PSYCH-ADS/xuqian_chen/YES_lab/Amber/nlp/Congress/model' #change to your own path
# models = load_word2vec_models(model_folder_path)
# null_lists = generate_random_words(foundations, 10000, models, tmp_folder_path, 'foundaiton_word10000',False)
# dfusnull_final = calculate_null_association(models, targets, foundations, null_lists,'us_trueword10000')

# China's People's Daily
chi_null_filepath = os.path.join(nullresults_folder_path, 'null10000_chi_all.csv')
# if os.path.exists(chi_null_filepath):
dfchinull_final = pd.read_csv(chi_null_filepath)
# else:
# model_chi_folder_path = '/home/local/PSYCH-ADS/xuqian_chen/Github/agebias-chi/0_data/model' #change to your own path
# models_chi = load_word2vec_models(model_chi_folder_path)
# null_lists_chi = generate_random_words(foundations_chi, 10000, models_chi, tmp_folder_path, 'foundaiton_chi_word10000',False)
# dfchinanull_final = calculate_null_association(models_chi, targets_chi, foundations_chi, null_lists_chi,'china_trueword10000')
dfus = pd.read_csv(os.path.join(pipeline_folder_path,'foundations_us.csv'))
dfus['efficiency_diff'] = dfus['efficiency_virtue'] - dfus['efficiency_vice']
dfus['effort_diff'] = dfus['effort_virtue'] - dfus['effort_vice']
dfusnull_final['effort_diff'] = dfusnull_final['effort_virtue'] - dfusnull_final['effort_vice']
dfusnull_final['efficiency_diff'] = dfusnull_final['efficiency_virtue'] - dfusnull_final['efficiency_vice']
dfusnull_lowerq = dfusnull_final.groupby(['year']).quantile(0.025)
dfusnull_upperq = dfusnull_final.groupby(['year']).quantile(0.975)

import matplotlib as mpl

# Set the global font to be Arial, size 18
mpl.rc('font', family='Arial', size=18)

sns.set_style("white")
sns.set_context("talk")  

# Create a figure with 2 rows and 1 column (i.e., two panels stacked vertically)
fig, ax = plt.subplots(2, 1, figsize=(12, 12))
effort_color = 'blue'
efficiency_color = 'green'
# First Plot (Effort and Efficiency) for dfus
ax[0].plot(dfus['year'], dfus['effort_virtue'] - dfus['effort_vice'], color=effort_color, label='Effort', linewidth=2)
ax[0].fill_between(dfus['year'], dfusnull_lowerq['effort_diff'], dfusnull_upperq['effort_diff'], color=effort_color, alpha=.1)
ax[0].plot(dfus['year'], dfus['efficiency_diff'], color=efficiency_color, label='Efficiency', linewidth=2)
ax[0].fill_between(dfus['year'], dfusnull_lowerq['efficiency_diff'], dfusnull_upperq['efficiency_diff'], color=efficiency_color, alpha=.1)
ax[0].set_title("Moral Values of Effort and Efficiency Over Time (US)", fontsize=20)
ax[0].text(-0.15, 1.05, 'A', transform=ax[0].transAxes, size=20, weight='bold')
ax[0].set_xlabel("Year", fontsize=18)
ax[0].set_ylabel("Embedding Bias (Virtue - Vice)", fontsize=18)
ax[0].tick_params(axis='both', labelsize=16)

# Second Plot (Inefficient Effort) for dfus
ax[1].plot(dfus['year'], dfus['effort_virtue'] - dfus['efficiency_virtue'], color='red', label='Inefficient Effort', linewidth=2)
ax[1].fill_between(dfus['year'], dfusnull_lowerq['effort_virtue'] - dfusnull_lowerq['efficiency_virtue'] , dfusnull_upperq['effort_virtue'] - dfusnull_upperq['efficiency_virtue'], color='red', alpha=.1)

ax[1].set_title("Moral Values of Inefficient Effort Over Time (US)", fontsize=20)
ax[1].set_xlabel("Year", fontsize=18)
ax[1].set_ylabel("Effort Virtue - Efficiency Virtue", fontsize=18)
ax[1].tick_params(axis='both', labelsize=16)
ax[1].text(-0.15, 1.05, 'B', transform=ax[1].transAxes, size=20, weight='bold')
ax[1].legend(loc='upper left')

# Shared aesthetics for both plots
for axis in ax:
    sns.despine(ax=axis)
    leg = axis.legend(loc='upper left', frameon=True, fontsize=16)
    leg.get_frame().set_edgecolor('black')

# Save as 300 ppi png
plt.tight_layout()
plt.savefig(os.path.join(bcp_null_path, 'combined_us_manuscript.png'), format='png', dpi=300)

# Combine the two plots
sns.set_style("white")
sns.set_context("talk")  

# Create a figure with 2 row and 1 columns (i.e., two panels up and down)
fig, ax = plt.subplots(2, 1, figsize=(12, 12))

## China
dfchi = pd.read_csv(os.path.join(pipeline_folder_path,'foundations_chi.csv'))
dfchinull_final['effort_diff'] = dfchinull_final['effort_virtue'] - dfchinull_final['effort_vice']
dfchinull_final['efficiency_diff'] = dfchinull_final['efficiency_virtue'] - dfchinull_final['efficiency_vice']
dfchinull_lowerq = dfchinull_final.groupby(['year']).quantile(0.025)
dfchinull_upperq = dfchinull_final.groupby(['year']).quantile(0.975)

# First Plot (Effort and Efficiency)
ax[0].plot(dfchi['year'], dfchi['effort_virtue'] - dfchi['effort_vice'], color=effort_color, label='Effort', linewidth=2)
ax[0].fill_between(dfchi['year'], dfchinull_lowerq['effort_diff'], dfchinull_upperq['effort_diff'], color=effort_color, alpha=.1)
ax[0].plot(dfchi['year'], dfchi['efficiency_virtue'] - dfchi['efficiency_vice'], color=efficiency_color, label='Efficiency', linewidth=2)
ax[0].fill_between(dfchi['year'], dfchinull_lowerq['efficiency_diff'], dfchinull_upperq['efficiency_diff'], color=efficiency_color, alpha=.1)
ax[0].set_title("Moral Values of Effort and Efficiency Over Time (China)", fontsize=20)
ax[0].set_ylim(-0.25, 0.6)
ax[0].set_xlabel("Year", fontsize=18)
ax[0].set_ylabel("Embedding Bias (Virtue - Vice)", fontsize=18)
ax[0].tick_params(axis='both', labelsize=16)
ax[0].text(-0.15, 1.05, 'A', transform=ax[0].transAxes, size=20, weight='bold')
# Second Plot (Inefficient Effort)
ax[1].plot(dfchi['year'], dfchi['effort_virtue'] - dfchi['efficiency_virtue'], color='red', label='Inefficient Effort', linewidth=2)
ax[1].fill_between(dfchi['year'], dfchinull_lowerq['effort_virtue'] - dfchinull_lowerq['efficiency_virtue'], dfchinull_upperq['effort_virtue'] - dfchinull_upperq['efficiency_virtue'], color='red', alpha=.1)
ax[1].set_title("Moral Values of Inefficient Effort Over Time (China)", fontsize=20)
ax[1].set_xlabel("Year", fontsize=18)
ax[1].set_ylabel("Effort Virtue - Efficiency Virtue", fontsize=18)
ax[1].tick_params(axis='both', labelsize=16)
ax[1].set_ylim(-0.25, 0.6)
ax[1].legend(loc='upper left')
ax[1].text(-0.15, 1.05, 'B', transform=ax[1].transAxes, size=20, weight='bold')
# Shared aesthetics for both plots
for axis in ax:
    sns.despine(ax=axis)
    leg = axis.legend(loc='upper left', frameon=True, fontsize=16)
    leg.get_frame().set_edgecolor('black')

# Save as 300 ppi png
plt.tight_layout()
plt.savefig(os.path.join(bcp_null_path, 'combined_china_manuscript.png'), format='png', dpi=300)
