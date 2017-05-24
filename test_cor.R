
library(Hmisc)

#########################################################################
# PART 1
#########################################################################

file_names <- read.table("./data/files_raw1.txt", stringsAsFactors = F, header = F)
file_names2 <- unlist(file_names)

f_count <- length(file_names2)
col_names <- c("fp1","fp2","f3","f4","f7",
               "f8","c3","c4","p3","p4",
               "o1","o2","t3","t4","t5",
               "t6","fz","cz","pz")

cr_all <- data.frame()

for (i in 1:f_count) {

  fn_raw <- file_names2[i]
  data_raw <- read.csv(paste0("./data/",fn_raw,".raw"))
  colnames(data_raw) <- col_names
  
  fn_art <- paste0("./data/",fn_raw,".art")
  if(file.exists(fn_art)) {
    data_art <- read.csv(fn_art)
    for (k in 1:19) {
      mask <- data_art[,k] == 1
      data_raw[mask,k] <- NA
    }
  }
  
  c_res <- c()
  cr <-rcorr(as.matrix(data_raw))$r
  #  cr <- cor(data_raw)
  for(j in 1:18){
      c_res <- c(c_res, cr[j, (j+1):19])
  }

  cr_all <- rbind(cr_all, c_res)
  row.names(cr_all)[i]<-fn_raw

  data_desc <- paste(i, fn_raw)
  print(data_desc)
}

cr_col_names <- c()
for (j in 1:18) {
  for (k in (j+1):19){
   cr_col_names <- c(cr_col_names, paste0(col_names[j],col_names[k]))
  }
}
colnames(cr_all) <- cr_col_names

# Save the CSV
write.csv(cr_all, "cor_data_cleaned.csv")

#########################################################################
# PART 2
#########################################################################
# read CSV again
cr_all <- read.csv("cor_data_cleaned.csv")
cr_row_names <- cr_all[,1]
cr_all <- cr_all[,2:172]
rownames(cr_all) <- cr_row_names

# Heatmap
heatmap(as.matrix(cr_all), Colv=NA)

# correct NA value
sapply(cr_all, function(x) sum(is.na(x)))
cr_all$f7t3[is.na(cr_all$f7t3)] <-0

# PCA
pca<-prcomp(cr_all)
print(pca)
plot(pca, type = "l")

# Read the labels file
labels <- read.csv("labels.csv")

pca_data <- as.data.frame(pca$x)
pca_data$fn <- rownames(pca_data)
# left join
pca_data <- merge(x = pca_data, y = labels, by = "fn", all.x = TRUE)

# detect outliers
library(anomalyDetection)
pca_data$md <- mahalanobis_distance(pca_data[,2:3])
pca_data$anomaly <- pca_data$md > 5

# plot
p <- ggplot(pca_data, aes(PC1, PC2, color=anomaly)) + geom_point() + 
  geom_text(aes(label = ifelse(anomaly==TRUE,as.character(fn),''), hjust=0, vjust=0))
p
