
library(neuralnet)
library(caret)
library(AppliedPredictiveModeling)

# read CSV
cr_all <- read.csv("cor_data_cleaned.csv")
cr_row_names <- cr_all[,1]
cr_all <- cr_all[,2:172]
rownames(cr_all) <- cr_row_names
cr_col_names <- colnames(cr_all)[2:172]

#generate input and output column names
cnames_inputs <- paste0(cr_col_names, "i")
cnames_outputs <- paste0(cr_col_names, "o")

train <- cr_all[,2:172]
train <- cbind(train, train)

colnames(train) <- c(cnames_inputs, cnames_outputs)

# Preprocess with caret package
preProcValues <- preProcess(train, method = c("range"))
train2 <- predict(preProcValues, train)

# formula for model
f <- as.formula(paste(paste(cnames_inputs, collapse = " + "), "~", paste(cnames_outputs, collapse = " + ")))

set.seed(0)
model1 <- neuralnet(f, train2, hidden=c(20,2,20), algorithm = 'rprop+', threshold = 0.1, learningrate = 0.7)
print (paste("MSE=", model1$result.matrix[1]))

#plot(model1)

results <- compute(model1, train2[,1:171]) #Run them through the neural network
results$net.result
inl <- as.data.frame(results$neurons[[3]][,2:3])
inl <- cbind(inl, iris[,5])
colnames(inl) <- c("HL1","HL2")

# Read the labels file
labels <- read.csv("labels.csv")

nn_data <- inl
nn_data$fn <- cr_all$X
# left join
nn_data <- merge(x = nn_data, y = labels, by = "fn", all.x = TRUE)

# detect outliers
library(anomalyDetection)
nn_data$HL1[is.na(nn_data$HL1)] <-0
nn_data$HL2[is.na(nn_data$HL2)] <-0

nn_data$md <- mahalanobis_distance(nn_data[,2:3])
nn_data$anomaly <- nn_data$md > 5

# plot with labeled ouliers
p <- ggplot(nn_data, aes(HL1, HL2, color=anomaly)) + geom_point() + 
  geom_text(aes(label = ifelse(anomaly==TRUE,as.character(fn),''), hjust=0, vjust=0))
p
