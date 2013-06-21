## CPD EDA

setwd("~/Data Science for Social Good/CPD/Crime Data")
data = read.csv("Crimes_-_2001_to_present.csv")

############
#Splitting up into Crime Type Datasets
############
load#Subset the top ten most common types of primary crime
#Most Common = THEFT
theft.data.01to13 = data[which(data[,6]=="THEFT"),] #the most common Primary type of crime
write.csv(theft.data.01to13, file = "theft01.to.13.csv")
# Second Most Common = BATTERY
battery.data.01to13 = data[which(data[,6]=="BATTERY"),]
write.csv(battery.data.01to13, file = "battery01.to.13.csv")
# Third Most Common = CRIMINAL DAMAGE
cdamage.data.01to13 = data[which(data[,6]=="CRIMINAL DAMAGE"),] 
write.csv(cdamage.data.01to13, file = "cdamage01.to.13.csv")
# Fourth Most Common = NARCOTICS
narcotics.data.01to13 = data[which(data[,6]=="NARCOTICS"),] 
write.csv(narcotics.data.01to13, file = "narcotics01.to.13.csv")
# Fifth Most Common = OTHER OFFENSE
# Sixth Most Common = BURGLARY
burglary.data.01to13 = data[which(data[,6]=="BURGLARY"),] 
write.csv(burglary.data.01to13, file = "burglary01.to.13.csv")
# Seventh Most Common =  ASSAULT
assault.data.01to13 = data[which(data[,6]=="ASSAULT"),] 
write.csv(assault.data.01to13, file = "assaut01.to.13.csv")
# Eighth Most = MOTOR VEHICLE THEFT
vtheft.data.01to13 = data[which(data[,6]=="MOTOR VEHICLE THEFT"),] 
write.csv(vtheft.data.01to13, file = "vtheft01.to.13.csv")
# Ninth Most = ROBBERY
robbery.data.01to13 = data[which(data[,6]=="ROBBERY"),]
write.csv(robbery.data.01to13, file = "robbery01.to.13.csv")
# Tenth Most = DECEPTIVE PRACTICE
dpractice.data.01to13 = data[which(data[,6]=="DECEPTIVE PRACTICE"),] 
write.csv(dpractice.data.01to13, file = "dpractice01.to.13.csv")
# HOMICIDE (just doing for interest; not one of the top ten most common)
homicide.data.01to13 = data[which(data[,6]=="HOMICIDE"),] 
write.csv(homicide.data.01to13, file = "homicide01.to.13.csv")

############
## To get hours past midnight for each of these crime type datasets
# 2001-2013 Chicago Crime Portal Data Modifications
############
#Import dataset
setwd("~/Data Science for Social Good/CPD/Crime Data")
robbery.data = read.csv("robbery01.to.13.csv")
attach(robbery.data) #other features masked

#Run this conversion function
time = numeric()
convert.to.military = function(input.factor){
  temp1 = as.numeric(substr(input.factor, 1, 2))
  temp2 = as.numeric(substr(input.factor, 4, 5))/60
  if (temp1-12 == 0) {temp1 = 0} 
  if (substr(input.factor, 10, 11) == "AM"){
    time = as.numeric(temp1 + temp2)
  }
  if(substr(input.factor, 10, 11) == "PM"){
    time = as.numeric(12 + temp1 + temp2)
  }
  paste(time)
}

## TIME DISTRIBUTION ANALYSIS
time = numeric()
for(i in 1:dim(robbery.data[1])){
  y = substr(robbery.data$Date[i], 12, 23)
  time[i] = convert.to.military(y)
  if(i%%1000==0) print(i)
}

#Update Dataset
robbery.data = cbind(robbery.data, time)
#Save Dataset
write.csv(robbery.data, file = "robbery.data.csv")

############
# Exploratory Data Analysis
############
#Attach datasets
setwd("~/Data Science for Social Good/CPD/Crime Data/Datasets")
assault.data = read.csv("assault.data.csv")
battery.data = read.csv("battery.data.csv")
burglary.data = read.csv("burglary.data.csv")
cdamage.data = read.csv("cdamage.data.csv")
dpractice.data = read.csv("dpractice.data.csv")
homicide.data = read.csv("homicide.data.csv")
narcotics.data = read.csv("narcotics.data.csv")
robbery.data = read.csv("robbery.data.csv")
theft.data = read.csv("theft.data.csv")
vtheft.data = read.csv("vtheft.data.csv")
domestic.violence.data = read.csv("Domestic Violence.csv")

## Time distribution Analyses
plot(density(assault.data$time), col = "red", lwd = 2, 
     xlab = "Hours After Midnight",
     main = "Crime-Specific Time Distributions",
     ylim = c(0, 0.105)) #violent
mtext("2001-2013 Chicago Crime Portal Data")
lines(density(battery.data$time), col = "blue", lwd =2)  #not violent
lines(density(burglary.data$time), col = "green", lwd =2) #not violent
lines(density(cdamage.data$time), col = "purple", lwd =2) #not violent
lines(density(dpractice.data$time), col = "orange", lwd =2) #not violent
lines(density(homicide.data$time), col = "black", lwd =2) #violent
lines(density(narcotics.data$time), col = "pink", lwd =2) #not violent
lines(density(robbery.data$time), col = "brown", lwd =2) #not violent
lines(density(theft.data$time), col = "gray", lwd =2) #not violent
lines(density(vtheft.data$time), col = "yellow", lwd =2) #not violent
lines(density(domestic.violence.data$time), col = "navajowhite3", lwd =2) # violent
legend("topleft", c("Assault", "Battery", "Burglary", 
                    "Criminal Damage", "Deceptive Practice",
                    "Homicide", "Narcotics", "Robbery", "Theft", 
                    "Vehicle Theft", "Domestic Violence"), cex = 0.5, 
       col=c("red", "blue", "green", "purple", "orange",
             "black", "pink", "brown", "gray", "yellow", "navajowhite3"), lwd=2)


## Visualize spatial relationships within the city

#Homicide
for(j in 1:1){
  plot(homicide.data$X.Coordinate[rev(homicide.data$X)[j]],
       homicide.data$Y.Coordinate[rev(homicide.data$X)[j]],
       xlim = c(min(homicide.data$X.Coordinate), max(homicide.data$X.Coordinate)),
       ylim = c(min(homicide.data$Y.Coordinate), max(homicide.data$Y.Coordinate)),
       pch = 16, col = "gray")
  Sys.sleep(1)
}
par(new = TRUE)
  for(j in 1001:1300){
    points(homicide.data$X.Coordinate[rev(homicide.data$X)[j]],
         homicide.data$Y.Coordinate[rev(homicide.data$X)[j]], col = "red", lwd = 3, pch = 16)
    Sys.sleep(.3)
    points(homicide.data$X.Coordinate[rev(homicide.data$X)[j]],
           homicide.data$Y.Coordinate[rev(homicide.data$X)[j]], pch = 16, col = "light blue")
  }
 #par(new = TRUE)
par(new = FALSE)

#Domestic Violence
#for(j in 1:1){
#  plot(domestic.violence.data$X.Coordinate[rev(domestic.violence.data$X)[j]],
#       domestic.violence.data$Y.Coordinate[rev(domestic.violence.data$X)[j]],
#       xlim = c(min(domestic.violence.data$X.Coordinate), max(domestic.violence.data$X.Coordinate)),
#       ylim = c(min(domestic.violence.data$Y.Coordinate), max(domestic.violence.data$Y.Coordinate)),
#       pch = 16, col = "gray")
#  Sys.sleep(1)
#}
#par(new = TRUE)
#for(j in 2:450){
#  points(domestic.violence.data$X.Coordinate[rev(domestic.violence.data$X)[j]],
#         domestic.violence.data$Y.Coordinate[rev(domestic.violence.data$X)[j]], col = "red", lwd = 3, pch = 16)
#  Sys.sleep(.3)
#  points(domestic.violence.data$X.Coordinate[rev(domestic.violence.data$X)[j]],
#         domestic.violence.data$Y.Coordinate[rev(domestic.violence.data$X)[j]], pch = 16, col = "light gray")
#}
##par(new = TRUE)
#par(new = FALSE)domestic.violence


#Assault
# Will need: length(which(assault.data$X.Coordinate!="NA"))
#for(j in 1:1){
#  plot(assault.data$X.Coordinate[rev(assault.data$X)[j]],
#       assault.data$Y.Coordinate[rev(assault.data$X)[j]],
#       xlim = c(min(assault.data$X.Coordinate), max(assault.data$X.Coordinate)),
#       ylim = c(min(assault.data$Y.Coordinate), max(assault.data$Y.Coordinate)),
#       pch = 16, col = "gray")
#  Sys.sleep(1)
#}
#par(new = TRUE)
#for(j in 2:450){
#  points(assault.data$X.Coordinate[rev(assault.data$X)[j]],
#         assault.data$Y.Coordinate[rev(assault.data$X)[j]], col = "red", lwd = 3, pch = 16)
#  Sys.sleep(.3)
#  points(assault.data$X.Coordinate[rev(assault.data$X)[j]],
#         assault.data$Y.Coordinate[rev(assault.data$X)[j]], pch = 16, col = "light gray")
#}
#par(new = TRUE)
#par(new = FALSE)



##########
# Heatmaps: Hexagon plots
##########
a<-assault.data$X.Coordinate
b<-assault.data$Y.Coordinate
library(hexbin)
plot(hexbin(a,b), main = "Assault")

a<-homicide.data$X.Coordinate
b<-homicide.data$Y.Coordinate
library(hexbin)
plot(hexbin(a,b), main ="Homicide")

a<-narcotics.data$X.Coordinate
b<-narcotics.data$Y.Coordinate
library(hexbin)
plot(hexbin(a,b), main = "Narcotics")

a<-cdamage.data$X.Coordinate
b<-cdamage.data$Y.Coordinate
library(hexbin)
plot(hexbin(a,b), main = "Criminal Damage")

a<-robbery.data$X.Coordinate
b<-robbery.data$Y.Coordinate
library(hexbin)
plot(hexbin(a,b), main = "Robbery")

a<-theft.data$X.Coordinate
b<-theft.data$Y.Coordinate
library(hexbin)
plot(hexbin(a,b), main = "Theft")

a<-vtheft.data$X.Coordinate
b<-vtheft.data$Y.Coordinate
library(hexbin)
plot(hexbin(a,b), main = "Vehicular Theft")


#############
# Code I'm still working on
#############
# A: this works to show the shapefile, but it doesn't match X and Y Coordinates
install.packages("spdep")
library(spdep)  
ccShape=readShapePoly('~/Data Science for Social Good/CPD/Shapefiles/cpd_districts/cpd_districts.shp') # here cbg00barncnty is an ArcGIS shapefile  
plot(ccShape)
par(new = TRUE)
plot(homicide.data$Longitude[1:10], homicide.data$Latitude[1:10],
     pch = 16)
par(new = FALSE)
#     ,add=T,lwd=lwd,border='grey') # ,col='lightgrey') # this assumes you've already plotted some data based on coordinates in the projection of the shapefile  
#Or, to plot the regions in a new plot:  
#  plot(ccShape) # plot the regions 

# B: Doesn't work
library("maptools")
x = read.shape(system.file("~/Data Science for Social Good/CPD/Shapefiles/cpd_districts/cpd_districts.shp"),
               package="maptools")

# C: ggplot 2 time series visualization
install.packages("ggplot2")
library(ggplot2)
qplot(homicide.data$X.Coordinate, homicide.data$Y.Coordinate, 
      data=homicide.data, colour = rev(homicide.data$X))

#install.packages("ggplot2")
#library(ggplot2)
#qplot(x, y, data=graphdata, colour = size)
#qplot(x, y, data=graphdata, size = size)
#qplot(x, y, data=graphdata, full = size, geom="tile")