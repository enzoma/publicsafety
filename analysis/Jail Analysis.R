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
JailData <- read.csv("~/Data Science for Social Good/CPD/Crime Data/Jail Data/JailData.csv", header=TRUE)
View(JailData)
data = cbind(data, JailData$unique_id, JailData$arrest.count)
View(data)
data = JailDataJuly20.1
View(data)

Compiled.Jail.Data <- read.csv("~/Data Science for Social Good/CPD/Crime Data/Jail Data/Compiled.Jail.Data.csv")
View(Compiled.Jail.Data)
data = Compiled.Jail.Data
names(data)

arrest.count.col=numeric()
for(i in 1:dim(data)[1]){
  arrest.count.col[which(data$InmateName==paste(data$InmateName[i]))]=  
    length(which(data$InmateName==paste(data$InmateName[i])))
  if(i%%100==0) print(i)
}

dates_of_interest <- read.csv("~/Data Science for Social Good/CPD/Crime Data/Jail Data/dates_of_interest.csv")
#  View(dates_of_interest)
data = cbind(data, arrest.count.col, dates_of_interest$days_of_stay, dates_of_interest$age_in_years_at_arrest)
write.csv(data, file = "JailData.csv")
JailData <- read.csv("~/Data Science for Social Good/CPD/Crime Data/Jail Data/JailData.csv")
View(JailData)
data = JailData
View(data)
names(data)[14] = "total.arrest.count"
names(data)[15]="days_of_stay"
names(data)[16]="age_at_arrest"

## Resolving blank unique_id fields
need.to.fill = which(data$unique_id=="\\N")
replacement.fields = numeric()

for(i in 1:length(need.to.fill)){
  replacement.fields = intersect(
    which(data$InmateName==paste(data$InmateName[need.to.fill[i]])),
    which(data$BirthDate==paste(data$BirthDate[need.to.fill[i]]))
  )
  data$unique_id[replacement.fields] = 137935 + 1 + i
  if(i%%100==0) cat(i, print(Sys.time()))
}


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


### Age at Arrest ###
# Convert age field to numeric
data$age = as.numeric(levels(data$age))[data$age]
hist(data$age, 
     main = "Age at Arrest: All Cases", xlab = "Age")
mtext("Cook County Sheriff's Office Jail Data")

hist(data$age[which(data$ChargeCode=="720 ILCS 570/402(c)")],
     main = "Age at Arrest: ILCS 720 ILCS 570/402(c)", xlab = "Age")
mtext("POSS AMT CON SUB EXCEPT(A)/(D)")

hist(data$age[which(data$ChargeCode=="625 ILCS 5/6-303(a)")],
     main = "Age at Arrest: ILCS 625 ILCS 5/6-303(a)", xlab = "Age")
mtext("DRVING ON REVOK OR SUSP DUI/SSS ALL")

hist(data$age[which(data$ChargeCode=="720 ILCS 5/12-3.2(a)(1)")],
     main = "Age at Arrest: ILCS 720 ILCS 5/12-3.2(a)(1)", xlab = "Age")
mtext("DOMESTIC BATTERY/BODILY HARM/VIOLATION O/P")

hist(data$age[which(data$ChargeCode=="720 ILCS 5/16A-3(a)")],
     main = "Age at Arrest: ILCS 720 ILCS 5/16A-3(a)", xlab = "Age")
mtext("RETAIL THEFT:WITH INTENT TO RETAIN/DEPRIVE")

hist(data$age[which(data$ChargeCode=="625 ILCS 5/11-501(a)")],
     main = "Age at Arrest: ILCS 625 ILCS 5/11-501(a)", xlab = "Age")
mtext("DUI/INTOXICATING COMPOUND")


## Weed Analysis 
hist(data$age[which(data$ChargeCode=="720 ILCS 550/4(a)")],
     main = "Age at Arrest: ILCS 720 ILCS 550/4(a)", xlab = "Age")
mtext("ILLEGAL POSSESSION OF CANNABIS:2.5 GRAMS OR LESS")

hist(data$age[which(data$ChargeCode=="720 ILCS 550/4(b)")],
     main = "Age at Arrest: ILCS 720 ILCS 550/4(b)", xlab = "Age")
mtext("ILLEGAL POSSESSION OF CANNABIS:2.5 TO 10 GRAMS")

hist(data$age[which(data$ChargeCode=="720 ILCS 550/4(c)")],
     main = "Age at Arrest: ILCS 720 ILCS 550/4(c)", xlab = "Age")
mtext("ILLEGAL POSSESSION OF CANNABIS:10 TO 30 GRAMS")

hist(data$age[which(data$ChargeCode=="720 ILCS 550/4(d)")],
     main = "Age at Arrest: ILCS 720 ILCS 550/4(d)", xlab = "Age")
mtext("ILLEGAL POSSESSION OF CANNABIS:30 TO 500 GRAMS")


### Length of Stay Analysis ###
# Convert to numeric
data$days_of_stay = as.numeric(levels(data$days_of_stay))[data$days_of_stay]
data$unique_id = as.numeric(levels(data$unique_id))[data$unique_id]

data$days_of_stay[which(data$days_of_stay < 0)] = 0 #assign negative values to 0

hist(data$days_of_stay, 
     main = "Length of Stay: All Cases", xlab = "Length of Stay (days)",
     col = "mistyrose2")
mtext("Cook County Sheriff's Office Jail Data")

hist(data$days_of_stay[which(data$ChargeCode=="720 ILCS 570/402(c)")],
     main = "Length of Stay: ILCS 720 ILCS 570/402(c)", xlab = "Length of Stay (days)",
     col = "mistyrose2")
mtext("POSS AMT CON SUB EXCEPT(A)/(D)")

hist(data$days_of_stay[which(data$ChargeCode=="625 ILCS 5/6-303(a)")],
     main = "Length of Stay: ILCS 625 ILCS 5/6-303(a)", 
     xlab = "Length of Stay (days)", col = "mistyrose2")
mtext("DRVING ON REVOK OR SUSP DUI/SSS ALL")

hist(data$days_of_stay[which(data$ChargeCode=="720 ILCS 5/12-3.2(a)(1)")],
     main = "Length of Stay: ILCS 720 ILCS 5/12-3.2(a)(1)", 
     xlab = "Length of Stay (days)", col = "mistyrose2")
mtext("DOMESTIC BATTERY/BODILY HARM/VIOLATION O/P")

hist(data$days_of_stay[which(data$ChargeCode=="720 ILCS 5/16A-3(a)")],
     main = "Length of Stay: ILCS 720 ILCS 5/16A-3(a)", 
     xlab = "Length of Stay (days)", col = "mistyrose2")
mtext("RETAIL THEFT:WITH INTENT TO RETAIN/DEPRIVE")

hist(data$days_of_stay[which(data$ChargeCode=="625 ILCS 5/11-501(a)")],
     main = "Length of Stay: ILCS 625 ILCS 5/11-501(a)", 
     xlab = "Length of Stay (days)", col = "mistyrose2")
mtext("DUI/INTOXICATING COMPOUND")

## Weed Analysis 
hist(data$days_of_stay[which(data$ChargeCode=="720 ILCS 550/4(a)")],
     main = "Length of Stay: ILCS 720 ILCS 550/4(a)", 
     xlab = "Length of Stay (days)", ylab = "Length of Stay (days)", col = "mistyrose2")
mtext("ILLEGAL POSSESSION OF CANNABIS:2.5 GRAMS OR LESS")

hist(data$days_of_stay[which(data$ChargeCode=="720 ILCS 550/4(b)")],
     main = "Length of Stay: ILCS 720 ILCS 550/4(b)", 
     xlab = "Length of Stay (days)", ylab = "Length of Stay(days)", col = "mistyrose2")
mtext("ILLEGAL POSSESSION OF CANNABIS:2.5 TO 10 GRAMS")

hist(data$days_of_stay[which(data$ChargeCode=="720 ILCS 550/4(c)")],
     main = "Length of Stay: ILCS 720 ILCS 550/4(c)", ylab = "Length of Stay (days)" 
     xlab = "Length of Stay (days)", col = "mistyrose2")
mtext("ILLEGAL POSSESSION OF CANNABIS:10 TO 30 GRAMS")

hist(data$days_of_stay[which(data$ChargeCode=="720 ILCS 550/4(d)")],
     main = "Length of Stay: ILCS 720 ILCS 550/4(d)", 
     xlab = "Length of Stay (days)", ylab = "Length of Stay (days)", col = "mistyrose2")
mtext("ILLEGAL POSSESSION OF CANNABIS:30 TO 500 GRAMS")

## Length of Stay vs. Age
plot(data$age, data$days_of_stay, col = "navy", pch = ".",
     main = "Length of Stay vs. Age: All Cases", ylab = "Length of Stay (days)",
     xlab = "Age")

plot(data$age[which(data$ChargeCode=="720 ILCS 570/402(c)")],
     data$days_of_stay[which(data$ChargeCode=="720 ILCS 570/402(c)")],
     col = "navy", xlab = "Age", ylab = "Length of Stay(days)",
     main = "Length of Stay vs. Age: 720 ILCS 570/402(c)", pch = ".")
     mtext("POSS AMT CON SUB EXCEPT(A)/(D)")
                  
plot(data$age[which(data$ChargeCode=="625 ILCS 5/6-303(a)")],
     data$days_of_stay[which(data$ChargeCode=="625 ILCS 5/6-303(a)")],
     col = "navy", xlab = "Age", ylab = "Length of Stay(days)",
     main = "Length of Stay vs. Age: 625 ILCS 5/6-303(a)", pch = ".")
mtext("DRVING ON REVOK OR SUSP DUI/SSS ALL")

plot(data$age[which(data$ChargeCode=="720 ILCS 5/12-3.2(a)(1)")],
     data$days_of_stay[which(data$ChargeCode=="720 ILCS 5/12-3.2(a)(1)")],
     col = "navy", xlab = "Age", ylab = "Length of Stay(days)",
     main = "Length of Stay vs. Age: 720 ILCS 5/12-3.2(a)(1)", pch = ".")
mtext("DOMESTIC BATTERY/BODILY HARM/VIOLATION O/P")

plot(data$age[which(data$ChargeCode=="720 ILCS 5/16A-3(a)")],
     data$days_of_stay[which(data$ChargeCode=="720 ILCS 5/16A-3(a)")],
     col = "navy", xlab = "Age", ylab = "Length of Stay(days)",
     main = "Length of Stay vs. Age: 720 ILCS 5/16A-3(a)", pch = ".")
mtext("RETAIL THEFT:WITH INTENT TO RETAIN/DEPRIVE")

plot(data$age[which(data$ChargeCode=="625 ILCS 5/11-501(a)")],
     data$days_of_stay[which(data$ChargeCode=="625 ILCS 5/11-501(a)")],
     col = "navy", xlab = "Age", ylab = "Length of Stay(days)",
     main = "Length of Stay vs. Age: 625 ILCS 5/11-501(a)", pch = ".")
mtext("DUI/INTOXICATING COMPOUND")

## Weed Analysis
plot(data$age[which(data$ChargeCode=="720 ILCS 550/4(a)")],
     data$days_of_stay[which(data$ChargeCode=="720 ILCS 550/4(a)")],
     main = "Age at Arrest: ILCS 720 ILCS 550/4(a)", xlab = "Age", pch = ".", 
     col = "navy", ylab = "Length of Stay (days)")
mtext("ILLEGAL POSSESSION OF CANNABIS:2.5 GRAMS OR LESS")

plot(data$age[which(data$ChargeCode=="720 ILCS 550/4(b)")],
     data$days_of_stay[which(data$ChargeCode=="720 ILCS 550/4(b)")],
     main = "Age at Arrest: ILCS 720 ILCS 550/4(b)", xlab = "Age", pch = ".", 
     col = "navy", ylab = "Length of Stay (days)")
mtext("ILLEGAL POSSESSION OF CANNABIS:2.5 TO 10 GRAMS")

plot(data$age[which(data$ChargeCode=="720 ILCS 550/4(c)")],
     data$days_of_stay[which(data$ChargeCode=="720 ILCS 550/4(c)")],
     main = "Age at Arrest: ILCS 720 ILCS 550/4(c)", xlab = "Age", pch = ".",
     col = "navy", ylab = "Length of Stay (days)")
mtext("ILLEGAL POSSESSION OF CANNABIS:10 TO 30 GRAMS")

plot(data$age[which(data$ChargeCode=="720 ILCS 550/4(d)")],
     data$days_of_stay[which(data$ChargeCode=="720 ILCS 550/4(d)")],
     main = "Age at Arrest: ILCS 720 ILCS 550/4(d)", xlab = "Age", pch = ".",
     col = "navy", ylab = "Length of Stay (days)")
mtext("ILLEGAL POSSESSION OF CANNABIS:30 TO 500 GRAMS")


### Bond Amounts for Repeat Offenders
# Convert to numeric
data$arrest_count_sql = as.numeric(levels(data$arrest_count_sql))[data$arrest_count_sql]
# Converting to Date Object: Adapt this code
# d <- as.POSIXlt(as.Date('2010/03/17'))
# d$year <- d$year-2
# as.Date(d)

# Assign person w/ > 54 arrests unique_id = 54
data$unique_id[which(data$arrest_count_sql>54)]

plot(data$CurrentBond[which(data$unique_id==54)], 
     col = "purple", pch = 16, type = "o", lwd = 0.4, xlim = c(0, 55),
     ylim = c(0, 80000), ylab = "Bond Amount ($)", xlab = "Arrest Count",
     main = "Bond Amount vs. Arrest Count")
mtext("Three most active criminals")
par(new = TRUE)
points(data$CurrentBond[which(data$unique_id==34865)], 
     col = "blue", pch = 16, type = "o", lwd = 0.4, xlim = c(0, 55), xaxt = "n",
     ylim = c(0, 80000), yaxt = 'n')
points(data$CurrentBond[which(data$unique_id==141162)],
       col = "lightgreen", pch = 16, type = "o", lwd = 0.4, xlim = c(0, 55), xaxt = "n",
       ylim = c(0, 80000), yaxt = 'n')
legend("topright", c("Indiv. 54", "Indiv. 34865", "Indiv. 141162"),
       col = c("purple", "blue", "lightgreen"), pch = 16, cex = 0.75)

## Attempt to show dates on x axis
axis.Date(1, at = seq(data$BookingDate[which(data$arrest_count_sql>54)][1], 
                      data$BookingDate[which(data$arrest_count_sql>54)][55], 
                      length.out=25),
          labels = seq(data$BookingDate[which(data$arrest_count_sql>54)][1], 
                       data$BookingDate[which(data$arrest_count_sql>54)][55], 
                       length.out=25),
          format= "%m/%d/%Y", las = 2)

## ## ## ## ## ## ## #### ## ## #### ## ## #### ## ## #### ## ## #### ## ## ##
# TO DO: See if the charge codes/descriptions for the big criminals 
# (ie, > 30 previous arrests) are the same or if these vary.  Also, it'd be interesting
# to see if their bonds increase after getting arrested more and more times

### Bond Amounts
# Comparison of Overall Non-0 Bond Amounts of those with low vs. high arrest count
hist(JD_1_RData$CurrentBond[which(JD_1_RData$CurrentBond!=0)])
## ## ## #### ## ## #### ## ## #### ## ## #### ## ## #### ## ## #### ## ## ##

