# Normalize Data
setwd("~/Data Science for Social Good/CPD/From_GitHub/dssg-cpd-project/clustering/version 2")
crime_by_tract_per_thousand <- read.csv("~/Data Science for Social Good/CPD/From_GitHub/dssg-cpd-project/clustering/version 2/crime_by_tract_per_thousand.csv")
View(crime_by_tract_per_thousand)
col.to.omit = c(1, 3, 6, 9, 10, 13, 14, 27, 30, 34) #omit tract number!
new = crime_by_tract_per_thousand[,-col.to.omit]
scaled.dat <- scale(new)
# check that we get mean of 0 and sd of 1
colMeans(scaled.dat)  # faster version of apply(scaled.dat, 2, mean)
apply(scaled.dat, 2, sd)
# Data have been normalized.  Now export
data = as.data.frame(cbind(crime_by_tract_per_thousand$tract, scaled.dat))
names(data)[1]="tract"
write.csv(data, file = "V2_normalized_crime_by_tract_per_thousand.csv")

###### Formatting CSV for Input into TileMill
`v2_normalized_clustering_with_geo` <- read.table("~/Data Science for Social Good/CPD/From_GitHub/dssg-cpd-project/clustering/version 2/v2_normalized_clustering_with_geo.csv", sep=";", quote="\"")
View(`v2_normalized_clustering_with_geo`)
write.csv(`v2_normalized_clustering_with_geo`, 
          file = "v2_normalized_clustering_with_geo.csv")