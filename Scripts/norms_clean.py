import pandas as pd
import tabula

# 1. Make affective_norms.csv
affective_df = pd.read_csv('../Norms/BRM-emot-submit.csv', index_col=0)
affective_df = affective_df[['Word','V.Mean.Sum','A.Mean.Sum','D.Mean.Sum']]
affective_df.columns = ['word','v','a','d']
affective_df.to_csv('../CSVNorms/affective_norms.csv')

# 2. Make imageability_norms.csv
imageability_df = tabula.read_pdf('../Norms/13428_2011_162_MOESM1_ESM.pdf', pages='all',pandas_options={'header':None})
imageability_df = pd.concat(imageability_df)
# Below, columns' names are what Schock et al. (2012) used
imageability_df.columns = ['item','mean_RT','sd_for_RT','mean_rating','sd_for_rating']
imageability_df = imageability_df[['item','mean_rating']]
imageability_df.columns = ['word','imageability']
imageability_df.to_csv('../CSVNorms/imageability_norms.csv')

# 3. Make frequency_norm.csv
frequency_df = pd.read_table('../Norms/Brysbaert-BRM-2009/SUBTLEXus74286wordstextversion.txt')
frequency_df = frequency_df[['Word', 'Lg10WF']]
frequency_df.columns = ['word','Lg10WF']
frequency_df.to_csv('../CSVNorms/frequency_norms.csv')

# 4. Make AOA_norms.csv
AOA_df = pd.read_excel('../Norms/13428_2013_348_MOESM1_ESM.xlsx')
AOA_df = AOA_df[['Word','Rating.Mean']]
AOA_df.columns = ['word', 'AOA']
AOA_df.to_csv('../CSVNorms/AOA_norms.csv')

# 5. Make intersect_norms.csv
intersect_df = pd.merge(pd.merge(pd.merge(affective_df, imageability_df, on = 'word'),
                frequency_df, on = 'word'),
                AOA_df, on = 'word')

# calculate word length in the orthographic form
word_len_li = []
for w in list(intersect_df['word']):
    word_len_li.append(len(w))
intersect_df['length'] = word_len_li

intersect_df.to_csv('../CSVNorms/intersect_norms.csv')

print(intersect_df.describe())

