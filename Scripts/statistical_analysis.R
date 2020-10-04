library(lme4)
library(optimx)
library(dplyr)

data <- read.csv('../Data/data_for_analysis.csv',
                      row.names=1)

#print(head(data))
#print(colnames(data))
# [1] "subjectID"           "listID"              "stimulus"
# [4] "response"            "correct_in_position" "item_correct"
# [7] "position"            "euc_dist_from_cent"  "v"
# [10] "a"                   "d"                   "imageability"
# [13] "Lg10WF"              "AOA"                 "length"

# Modifed varibales' type
data$subjectID <- as.factor(data$subjectID)
data$listID <- as.factor(data$listID)
data$stimulus <- as.factor(data$stimulus)

# Position in the origianl data starts from 0 (a convention for programming languages)
# Converts Position and make it start from 1 (for R language and natural languages :)
data$position <- data$position + 1
data$position <- as.factor(data$position)

print(str(data))

# Statistical Test
if(1){
# Correct-in-position scoring
  if(1){
      model <- glmer(correct_in_position ~ position +
                     euc_dist_from_cent +
                     length +
                     imageability + Lg10WF + AOA +
                     (1 | listID/stimulus) +
                     (1 | subjectID),
                     family='binomial',
                     control = glmerControl(optimizer = "bobyqa", calc.derivs = TRUE),
                     data=data)

      sink("../Results/corret_in_position_results.txt")
      print(summary(model))
      sink()
  }

# Item correct scoring
  if(1){
      model <- glmer(item_correct ~ position +
                     euc_dist_from_cent +
                     length +
                     imageability + Lg10WF + AOA +
                     (1 | listID/stimulus) +
                     (1 | subjectID),
                     family='binomial',
                     control = glmerControl(optimizer = "bobyqa", calc.derivs = TRUE),
                     data=data)
      sink("../Results/item_correct_results.txt")
      print(summary(model))
      sink()
  }

# Order errors scoring
# Order errors are words recalled at its wrong position, which can be defined as item correct - correct-in-position.
# Here, order errors reflect the absolute number of order errors that would be affected by item correct score
# Given that order errors are not observed unless words are recalled, the absolute number of order errors is meaningful if semantic similarity does not affect item correct.

  order_errors <- data$item_correct - data$correct_in_position
  data$order_errors <- order_errors

  if(1){
      model <- glmer(order_errors ~ position +
                     euc_dist_from_cent +
                     length +
                     imageability + Lg10WF + AOA +
                     (1 | listID/stimulus) +
                     (1 | subjectID),
                     family='binomial',
                     control = glmerControl(optimizer = "bobyqa", calc.derivs = TRUE),
                     data=data)

      sink("../Results/order_errors_results.txt")
      print(summary(model))
      sink()
  }
}
