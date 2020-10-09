# This script provide a plot of transposition gradients
# Check
# 1. Strong primacy effect
# 2. Weak recency effect
# 3. Transposition patters (e.g., locality constraint)

# For transposition_gradients, see Henson, R. N. A., Norris, D. G., Page, M. P. A., & Baddeley, A. D. (1996).
# Unchained Memory: Error Patterns Rule out Chaining Models of Immediate Serial Recall.
# The Quarterly Journal of Experimental Psychology Section A, 49(1), 80–115.
# https://doi.org/10.1080/713755612

library(dplyr)
library(ggplot2)
library(ggsci)

df <- read.csv('../Data/behav_data.csv')
df <- df[, colnames(df) != "X"]

df %>%
  group_by(subjectID) %>%
  summarise(n_distinct(listID))

# subject number = 114
# each subject took 25 trials
# 2850 (114 * 25) responses for each position

# row number = input position
# col number = output position
io_matrix <- matrix(0, nrow = 6, ncol = 6)

for(i in unique(df$subjectID)){
  single_sub_df <- df[df$subjectID == i, ]
  for(j in unique(single_sub_df$listID)){
    trial_df <- single_sub_df[single_sub_df$listID == j, ]
    for(one_stimulus in trial_df$stimulus){
      stimuli_position <- trial_df[trial_df$stimulus == one_stimulus, 'position'] + 1
      if(one_stimulus %in% trial_df$response){
        response_position <- trial_df[trial_df$response == one_stimulus, 'position'] + 1
        io_matrix[stimuli_position, response_position] <- io_matrix[stimuli_position, response_position] + 1
      }
    }
  }
}

# subject number = 114
# each subject took 25 trials
# 2850 (114 * 25) responses for each position
# Get rates
io_matrix <- io_matrix / 2850

print(io_matrix)

input_position <- c(rep('1',6),rep('2',6),rep('3',6),rep('4',6),rep('5',6),rep('6',6))
output_position <- rep(as.character(1:6),6)
rates <- NULL
for(i in 1:6){
  rates <- c(rates, io_matrix[i,])
}

plot_df <- data.frame(Input = input_position,
                      Output = output_position,
                      Rates = rates)
print(plot_df)

g <- ggplot(plot_df, aes(x = Output, y = Rates, fill = Input)) +
  geom_bar(stat = 'identity', position = 'dodge', width=0.9) +
  scale_fill_nejm() +
  theme(legend.key.size = unit(0.3, 'cm'),
        legend.text = element_text(color = 'grey30'),
        panel.background = element_blank(),
        axis.line=element_line(colour = 'black', size = 0.2),
        axis.ticks=element_line(colour = 'black', size = 0.2),
        panel.border = element_blank()) +
  scale_y_continuous(expand = c(0, 0), limits = c(0, 1.0)) +
ggsave('../Results/transposition_gradients.png', width=4.5, height=3)
