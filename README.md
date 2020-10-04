# semsim-stm-exp
Scripts for an online experiment testing the semantic similarity effect on short-term memory. A preprint (a manuscript reported before peer-review) is available here.

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

### Optional 1. Exploratory Analysis with Chebyshev distance

Use Chebyshev distance instead of Euclidean distance. The implicit assumption behind the adoption of Euclidean distance is that valence, arousal, and dominace are equally used in semantic similarity cognition. It is, however, possible that only the most salient value among them is used. For example, if arousal information of a word (e.g., "snake") is very salient and distinctive, valence and dominance information would be ignored. Chebyshev distance is used to address this possibility.

```
cd ../Misc
python cheby_calc.py
Rscript exploratory_cheby.R
```

### Optional 2. Check U-shaped serial position curve

Check U-shaped serial position curve.

```
Rscript serial_position_curve_check.R
```
![serial_position_curve](https://github.com/grocio/stm-semsim-effect/blob/master/Results/Serial_Position_Curve.png)
### Optional 3. Check homogeneity of lists regarding lexicon-semantic variables

```
python lexico_semantic_variables_check.py
```

### Optional 4. Check associative strength

```
bash data_cleansing.sh
python semantic_association_check.py
```
