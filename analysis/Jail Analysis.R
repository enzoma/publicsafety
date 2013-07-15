# Jail Analysis
setwd("~/Data Science for Social Good/CPD/Crime Data/Jail Data")

##############
# Data Import
##############
# NB: These file paths specify my local directory, but the relevant csv files are on the server
JailData1 <- read.csv("~/Data Science for Social Good/CPD/Crime Data/Jail Data/JailData1.csv")
View(JailData1)
JailData2 <- read.csv("~/Data Science for Social Good/CPD/Crime Data/Jail Data/JailData2.csv", header=TRUE)
View(JailData2)
JailData3 <- read.csv("~/Data Science for Social Good/CPD/Crime Data/Jail Data/JailData3.csv",  header = TRUE)
View(JailData3)
JD_1_RData <- read.csv("~/Data Science for Social Good/CPD/Crime Data/Jail Data/JailData1_forR.csv")
View(JD_1_RData)

###############################################################
# General Data Housekeeping and determining which dataset to use
###############################################################
names(JailData1)
names(JailData2)
names(JailData3)
names(JD_1_RData)

JD1_names = JailData1$InmateName
JD2_names = JailData2$Name
JD3_names = JailData3$Name


length(intersect(JD1_names, JD2_names))
length(intersect(JD1_names, JD3_names))
length(intersect(JD2_names, JD3_names))

#############################################
# NB: Decided to focus analysis on JD_1_RData
#############################################

# Determine Counts for each unique name in JD_1_RData
# NB: This took several hours to run, so I've uploaded a csv
# file with the output to the server.  See Arrest_Counts.csv
arrest.count = numeric()
arrest.table = table(JD_1_RData$InmateName)
inmate.names = unique(JD_1_RData$InmateName)
for(i in 1:length(unique(JD_1_RData$InmateName))){
  name_of_interest = inmate.names[i]
  arrest.count[i] = 
    length(which(JD_1_RData$InmateName == paste(inmate.names[i])))
  if(i%%100==0) cat(i, print(Sys.time()))
}

## ## ## ## ## ## ## ## ## ## ## ## 
## Number of Arrests Exploration
## ## ## ## ## ## ## ## ## ## ## ## 
# Histograms of Number of Arrests
par(new = FALSE)

hist(JailData2$Booked.Times[which(JailData2$Booked.Times!=0)],
     main = "Number of Previous Arrests", col = "lavender")
mtext("Cook County Sheriff's Office Jail Data: Dataset 2")

hist(JailData2$Booked.Times[which(JailData2$Booked.Times>5)],
     main = "Histogram for Individuals with > 5 Previous Arrests ", col = "blue")
mtext("Cook County Sheriff's Office Jail Data: Dataset 2")

hist(arrest.count, 
     main = "Number of Previous Arrests ", col = "lavender")
mtext("Cook County Sheriff's Office Jail Data")

hist(arrest.count[which(arrest.count>10)], 
    main = "Histogram for Individuals with > 10 Previous Arrests ", col = "lavender")
mtext("Cook County Sheriff's Office Jail Data")

hist(arrest.count[which(arrest.count>20)], 
     main = "Histogram for Individuals with > 20 Previous Arrests ", col = "lavender")
mtext("Cook County Sheriff's Office Jail Data")

hist(arrest.count[which(arrest.count>30)], 
     main = "Histogram for Individuals with > 30 Previous Arrests ", col = "lavender")
mtext("Cook County Sheriff's Office Jail Data")

### ILCS Code Analysis
plotdata = cumsum((as.numeric(rev(sort(table(data$ChargeCode)))))/sum(as.numeric(table(data$ChargeCode))))
ggplot(plotdata, aes(x=x.to.plot, y=y.to.plot)) +
  geom_point(shape=1, colour = "red") + labs(title="Proportion of Cumulative Ranked ILCS Crime Codes") +
  xlab("Code Rank (by Frequency)") +
  ylab("Cumulative Proportion of All Codes in Dataset")
