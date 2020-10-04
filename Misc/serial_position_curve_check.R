library(dplyr)

data <- read.csv('../Data/behav_data.csv',
                      row.names=1)

data$position <- data$position + 1

# Check U-shaped performance with a strong primacy effect
pdf("../Results/Serial_Position_Curve.pdf")
data %>%
  group_by(position) %>%
  summarize(Correct_Recall = mean(correct_in_position, na.rm =TRUE)) %>%
  plot(type="o", pch=19, bty = 'l',ylim = c(0.0, 1.0),
       ylab = "Correct Recall", xlab = "Serial Position")
dev.off()
