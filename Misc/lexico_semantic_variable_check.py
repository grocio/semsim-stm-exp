from scipy import stats
import pandas as pd
from decimal import Decimal, ROUND_HALF_UP

# Helper
def correct_round(float_n, digit_n='0.01'):
    return Decimal(float_n).quantize(Decimal(digit_n), rounding=ROUND_HALF_UP)

# Note. intersect_norms includes lexico-semantic variables
norms_df = pd.read_csv('../CSVNorms/intersect_norms.csv', index_col=0)
materials_df = pd.read_csv('../Data/materials.csv', index_col=0)

#Check on heterogenity of lists regarding lexico-semantic values
for target_var in ['v', 'a','d','imageability','Lg10WF','AOA','length']:
    target_var_val_li = []
    for listID_N in sorted(list(set(materials_df['listID']))):
        current_words = list(materials_df.query('listID == @listID_N')['word'])
        target_var_vals = list(norms_df[norms_df['word'].isin(current_words)][target_var])
        target_var_val_li.append(target_var_vals)

    F, p = stats.f_oneway(*target_var_val_li)
    print('ANOVA for {}\nF value = {} and p value = {}\n'.format(target_var,
                                                            correct_round(F), correct_round(p)))

"""
ANOVA for v
F value = 0.92 and p value = 0.69

ANOVA for a
F value = 1.14 and p value = 0.19

ANOVA for d
F value = 0.95 and p value = 0.61

ANOVA for imageability
F value = 1.03 and p value = 0.42

ANOVA for Lg10WF
F value = 0.83 and p value = 0.86

ANOVA for AOA
F value = 1.15 and p value = 0.17

ANOVA for length
F value = 1.05 and p value = 0.37
"""
