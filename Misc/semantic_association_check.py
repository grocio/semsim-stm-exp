import pandas as pd
import numpy as np
from tqdm import tqdm

association_df = pd.read_csv('../CSVNorms/cleansedStrength.csv', sep='\t')

print(association_df.head())

materials_df = pd.read_csv('../Data/materials.csv', index_col=0)

cue_available = 0
cue_not_available = 0
strength_li = []

current_max = 0.0

for listID_N in tqdm(sorted(list(set(materials_df['listID'])))):
    # Target six words in a list of listID_N
    current_df = materials_df.query('listID == @listID_N')
    for w1 in list(current_df['word']):
        if w1 in list(association_df['cue']):
            cue_available += 1
            for w2 in list(current_df['word']):
                # Exclude cases in which a cue word == a response word
                if not w1 == w2:
                    strength_df = association_df.query('cue  == @w1 & response == @w2')
                    if not strength_df.empty:
                        strength_val = float(strength_df['R123.Strength'])
                        strength_li.append(strength_val)
                        # Record max strength val, which will be updated
                        if strength_val > current_max:
                            print('Strength = {} for cue: {} -> response: {}'.format(strength_val,w1,w2))
                            current_max = strength_val
                    # If a cue doen not cue a response word, associative strength is 0
                    else:
                        strength_li.append(0)
        # If w1 is not in norms as a cue, strength value is not retrieved
        else:
            cue_not_available += 1

print('Mean value: {}'.format(np.mean(strength_li)))
print('Max value: {}'.format(max(strength_li)))
print('0 count: {} / {}'.format(sum([i == 0 for i in strength_li]), len(strength_li)))
print('cue_available: {}'.format(cue_available))
print('cue_not_available: {}'.format(cue_not_available))
print('Norms coverage: {}%'.format(100 * cue_available / (cue_available + cue_not_available)))

"""
Mean value: 5.436827154021706e-05
Max value: 0.0204778156996587
0 count: 2442 / 2460
cue_available: 492
cue_not_available: 108
Norms coverage: 82.0%
"""
