# semsim-stm-exp
Scripts for an online experiment testing the semantic similarity effect on short-term memory. A preprint (a manuscript reported before peer-review) is available at [https://psyarxiv.com/va5js](https://psyarxiv.com/va5js).

## Dependencie
python libraries: pandas, [tabula-py](https://github.com/chezou/tabula-py) (that requires Java runtime).

R libraries: lme4, optimx, dplyr.

Plus, runtime environment for Shell Script (I use bash but your preferred \*sh would be OK).

## Workflow
### Step1. Get word norms
Download norms (provided as electronic supplementary materials) and save them in `semantic-stm-experiment` directory.
1. Affective norms ([Warriner et al., 2013](https://doi.org/10.3758/s13428-012-0314-x))
2. Imageability norms ([Schock et al., 2012](https://doi.org/10.3758/s13428-011-0162-0))
3. Frequency norms ([Brysbaert & New, 2009](https://doi.org/10.3758/BRM.41.4.977))
4. Age-Of-Acquisition (AOA) norms ([Kuperman et al., 2012](https://doi.org/10.3758/s13428-013-0348-8))

You will get `BRM-emot-submit.csv`, `13428_2011_162_MOESM1_ESM.pdf`, `Brysbaert-BRM-2009`, and `13428_2013_348_MOESM1_ESM.xlsx`. `Brysbaert-BRM-2009` is a folder but don't worry. Just save it.

### Step 2. Make word norms usable
File types of The above-mentioned 4 datasets are various: csv, txt, xlsx, and pdf!
Transform these files into handy and usable csv files.
```
cd Scripts/
python norms_clean.py
```

### Step 3. Calculate distance from the centroid
Ishiguro and Saito ([2020](https://doi.org/10.3758/s13423-020-01815-7)) proposed (Euclidean) *distance from the centroid* as a semantic simialrity metric. In the current experiment, each list has six words. We can calculate the centroid of a list and each of six words has distance from that centroid (this distance depends on list composition). For detailed information about the distance from the centroid metric, see Ishiguro and Saito ([2020](https://doi.org/10.3758/s13423-020-01815-7)).
```
python behav_with_metric.py
```
You will get values of distance from the centroid for all 600 words that we used in the current experiment.

### Step 4. Analyse data

Test the semantic similarity effect on STM.

```
Rscript statistical_analysis.R
```

### Supplementary 1. Exploratory Analysis with Chebyshev distance

Use Chebyshev distance instead of Euclidean distance. The implicit assumption behind the adoption of Euclidean distance is that valence, arousal, and dominace are equally used in semantic similarity cognition. It is, however, possible that only the most salient value among them is used. For example, if arousal information of a word (e.g., "snake") is very salient and distinctive, valence and dominance information would be ignored. Chebyshev distance is used to address this possibility.

```
cd ../Misc
python cheby_calc.py
Rscript exploratory_cheby.R
```

### Supplementary 2. Check transposition gradients

Check locality constraint for error patterns. For accuracy, check primacy and recency effects (a strong primacy effect and weak recency effect for immediate serial recall).

```
Rscript transposition_gradients.R
```
![transposition_gradients](https://github.com/grocio/semsim-stm-exp/blob/main/Results/transposition_gradients.png)
### Supplementary 3. Check homogeneity of lists regarding lexicon-semantic variables

```
python lexico_semantic_variables_check.py
```

### Supplementary 4. Check associative strength
Word association norms by De deyne et al. ([2019](https://doi.org/10.3758/s13428-018-1115-7)) will be used. Visit [their research project webpage](https://smallworldofwords.org/en/project/research) and click SWOW-EN2008 assoc. strengths (R123). Move `strength.SWOW-EN.R123.csv` to `Norms` directory. Then,
```
bash data_cleansing.sh
python semantic_association_check.py
```

### Supplementary 5. Check correlations between lexical or semantic variables
```
Rscript lexsem_pairs_plot.R
```
![lexsem_pairs](https://github.com/grocio/semsim-stm-exp/blob/main/Results/pairsplot.png)

Correlation coefficients are, in general, weak or modest. So, it is unlikely that multicollinearlity affects statistical results.

## References
Brysbaert, M., & New, B. (2009). Moving beyond Kučera and Francis: A critical evaluation of current word frequency norms and the introduction of a new and improved word frequency measure for American English. Behavior Research Methods, 41(4), 977–990. doi: [10.3758/BRM.41.4.977](https://doi.org/10.3758/BRM.41.4.977)

De Deyne, S., Navarro, D. J., Perfors, A., Brysbaert, M., & Storms, G. (2019). The “Small World of Words” English word association norms for over 12,000 cue words. Behavior Research Methods, 51(3), 987–1006. doi: [10.3758/s13428-018-1115-7](https://doi.org/10.3758/s13428-018-1115-7)

Ishiguro, S., & Saito, S. (2020). The detrimental effect of semantic similarity in short-term memory tasks: A meta-regression approach. Psychonomic Bulletin & Review. doi: [10.3758/s13423-020-01815-7](https://doi.org/10.3758/s13423-020-01815-7)

Kuperman, V., Stadthagen-Gonzalez, H., & Brysbaert, M. (2012). Age-of-acquisition ratings for 30,000 English words. Behavior Research Methods, 44(4), 978–990. doi: [10.3758/s13428-012-0210-4](https://doi.org/10.3758/s13428-012-0210-4)

Schock, J., Cortese, M. J., & Khanna, M. M. (2012). Imageability estimates for 3,000 disyllabic words. Behavior Research Methods, 44(2), 374–379. doi: [10.3758/s13428-011-0162-0](https://doi.org/10.3758/s13428-011-0162-0)

Warriner, A. B., Kuperman, V., & Brysbaert, M. (2013). Norms of valence, arousal, and dominance for 13,915 English lemmas. Behavior Research Methods, 45(4), 1191–1207. doi: [10.3758/s13428-012-0314-x](https://doi.org/10.3758/s13428-012-0314-x)
