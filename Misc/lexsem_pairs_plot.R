library(ggplot2)
library(GGally)
library(dplyr)

norms_df <- read.csv('../CSVNorms/intersect_norms.csv', row.names = 1)

materials_df <- read.csv('../Data/materials.csv', row.names = 1)

for_euc_dist_df <- read.csv('../Data/data_for_analysis.csv', row.names = 1)
for_euc_dist_df <- for_euc_dist_df[, c('stimulus', 'euc_dist_from_cent')]
for_euc_dist_df <- for_euc_dist_df[!duplicated(for_euc_dist_df$euc_dist_from_cent), ]

merged_df <- merge(materials_df, norms_df,
                   all.x = TRUE,
                   by = 'word')

merged_df <- merge(merged_df, for_euc_dist_df,
                   all.x = TRUE,
                   by.x = 'word',
                   by.y = 'stimulus')

cols <- colnames(merged_df)
target_var_names <- cols[6:length(cols)]

plot_df <- merged_df[, target_var_names]
colnames(plot_df) <- c('Imageability', 'Frequency', 'AOA', 'Length', 'Distance')
plot_df <- plot_df %>% select(Distance, Imageability, Frequency, Length, AOA)

#print(round(cor(plot_df), digits=2))
#
#              Distance Imageability Frequency Length   AOA
# Distance         1.00         0.05      0.20   0.01 -0.09
# Imageability     0.05         1.00      0.16  -0.03 -0.52
# Frequency        0.20         0.16      1.00   0.03 -0.52
# Length           0.01        -0.03      0.03   1.00  0.04
# AOA             -0.09        -0.52     -0.52   0.04  1.00
#
# Correlation coefficients are, in general, weak or modest.
# Thus, it is unlikely that multicollinearlity affects statistical results.


# Pairs plot
g <- ggpairs(plot_df)

resfactor <- 3
png('../Results/pairsplot.png', width = 640*resfactor, height = 640*resfactor,
    res = 72*resfactor)
print(g)
dev.off()

pdf('../Results/pairsplot.pdf')
print(g)
dev.off()
