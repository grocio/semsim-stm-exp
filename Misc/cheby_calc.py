"""
This script is similar to ../Scripts/behav_with_metric.py.
This script uses Chebyshev distance for semantic similarity metric while behav_with_metric.py uses Euclidean dist.
It creates a single csv file 'data_for_exploratory_analysis.csv'
"""

import pandas as pd
import numpy as np
from scipy.spatial import distance

behav_df = pd.read_csv('../Data/behav_data.csv', index_col=0)
norms_df = pd.read_csv('../CSVNorms/intersect_norms.csv', index_col=0)
materials_df = pd.read_csv('../Data/materials.csv', index_col=0)

df_for_analysis = pd.DataFrame(index=[],columns= [])

for listID_N in sorted(list(set(materials_df['listID']))):
    current_words_df = materials_df.query('listID == @listID_N')
    current_words_df = pd.concat([current_words_df,
        pd.DataFrame(index=[], columns=['cheby_dist_from_cent'])])

    current_norms = norms_df[norms_df['word'].isin(list(current_words_df['word']))]

    centroid = (current_norms['v'].mean(),
                current_norms['a'].mean(),
                current_norms['d'].mean())

    colnames = list(current_words_df.columns)
    for i in range(len(current_words_df)):
        current_word = list(current_words_df['word'])[i]

        word_vad = (float(norms_df.query('word == @current_word')['v']),
                    float(norms_df.query('word == @current_word')['a']),
                    float(norms_df.query('word == @current_word')['d']))

        current_words_df.iat[i,colnames.index('cheby_dist_from_cent')]\
                = distance.chebyshev(word_vad, centroid)

    df_for_analysis = df_for_analysis.append(current_words_df, ignore_index=True)

df_for_analysis = df_for_analysis.drop('listID', axis=1)

df_for_analysis = pd.merge(behav_df, df_for_analysis,
        left_on = 'stimulus', right_on = 'word').drop('word', axis=1)

df_for_analysis = pd.merge(df_for_analysis, norms_df,
        left_on = 'stimulus', right_on = 'word').drop('word', axis=1)

df_for_analysis = df_for_analysis.sort_values(['subjectID','listID','position'])
df_for_analysis = df_for_analysis.reset_index(drop=True)
df_for_analysis.to_csv('../Data/data_for_exploratory_analysis.csv')
