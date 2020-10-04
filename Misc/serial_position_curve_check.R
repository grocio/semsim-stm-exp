library(dplyr)

data <- read.csv('../Data/data_for_analysis.csv',
                      row.names=1)

# Check U-shaped performance with a strong primacy effect
pdf("../Results/Serial_Position_Curve.pdf")
data %>%
  group_by(position) %>%
  summarize(Correct_Recall = mean(correct_in_position, na.rm =TRUE)) %>%
  plot(type="o", ylab = "Correct Recall", xlab = "Serial Position")
dev.off()
