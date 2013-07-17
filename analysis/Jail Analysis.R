############ Jail Analysis ###########
setwd("~/Data Science for Social Good/CPD/Crime Data/Jail Data")


### Data Import ####
# NB: These file paths specify my local directory, but the relevant csv files are on the server
JailData1 <- read.csv("~/Data Science for Social Good/CPD/Crime Data/Jail Data/JailData1.csv")
View(JailData1)
JailData2 <- read.csv("~/Data Science for Social Good/CPD/Crime Data/Jail Data/JailData2.csv", header=TRUE)
View(JailData2)
JailData3 <- read.csv("~/Data Science for Social Good/CPD/Crime Data/Jail Data/JailData3.csv",  header = TRUE)
View(JailData3)
JD_1_RData <- read.csv("~/Data Science for Social Good/CPD/Crime Data/Jail Data/JailData1_forR.csv")
View(JD_1_RData)
Cleaning_Jail_Data <- read.csv("~/Data Science for Social Good/CPD/Crime Data/Jail Data/Cleaning_Jail_Data.csv")
data = Cleaning_Jail_Data
 

##### General Data Housekeeping and determining which dataset to use ####
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

### NB: Decided to focus analysis on JD_1_RData, later updated to "data" ####
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

#### Number of Arrests Exploration #########
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

######## ILCS Code Analysis #######
# Create a table 
charge.code.table = cbind(sort(table(data$ChargeCode), decreasing = TRUE))
indiv.prop = 
  as.numeric(rev(sort(table(data$ChargeCode))))/sum(as.numeric(table(data$ChargeCode)))
cumulative.prop = 
  cumsum(as.numeric(rev(sort(table(data$ChargeCode)))))/sum(as.numeric(table(data$ChargeCode)))
charge.code.table = cbind(charge.code.table, indiv.prop, cumulative.prop)

# Save table to CSV
write.csv(charge.code.table, file = "Crime_Codes_of_Interest.csv", 
          col.names = TRUE)

# Get Descriptions of these Crime Codes
Crime_Codes_of_Interest =
  read.csv("~/Data Science for Social Good/CPD/Crime Data/Jail Data/Crime_Codes_of_Interest.csv")
crime.codes = Crime_Codes_of_Interest

description=character()
for(k in 1:dim(crime.codes)[1]){
  description[k] = (as.character((data$ChargeDescription[which(data$ChargeCode==
    paste(as.character(crime.codes$Crime.Code[k])))][1])))
  if(k%%100==0) print(k)
}

# Now append these to the crime.codes table
crime.codes = cbind(charge.code.table, description)

# Save this new table
write.csv(crime.codes, file = "Crime_Codes_of_Interest_Final.csv",
          col.names = TRUE)

# Create a Graph
library(ggplot2)
plotdata = as.data.frame(cbind(x = seq(1:length(cumulative.prop)), y = cumulative.prop))
ggplot(plotdata, aes(x=x, y=cumulative.prop)) +
  geom_point(shape=1, colour = "navy") + labs(title="Proportion of Cumulative Ranked ILCS Crime Codes") +
  xlab("Code Rank (by Frequency)") +
  ylab("Cumulative Proportion of All Codes in Dataset")




## ## ## ## ## ## ## #### ## ## #### ## ## #### ## ## #### ## ## #### ## ## ##
# TO DO: See if the charge codes/descriptions for the big criminals 
# (ie, > 30 previous arrests) are the same or if these vary.  Also, it'd be interesting
# to see if their bonds increase after getting arrested more and more times

### Bond Amounts
# Comparison of Overall Non-0 Bond Amounts of those with low vs. high arrest count
hist(JD_1_RData$CurrentBond[which(JD_1_RData$CurrentBond!=0)])
## ## ## #### ## ## #### ## ## #### ## ## #### ## ## #### ## ## #### ## ## ##

