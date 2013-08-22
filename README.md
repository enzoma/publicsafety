DSSG: Crime and Incarceration
===
This is a [Data Science for Social Good]("http://www.dssg.io/") project to assess the burden groups of jail inmates pose to Chicago's crime problem in order to help the Cook County Jail to relieve its overcrowding problem and to explore predictors of violent crime.
The problem: 
===
Among the many [problems]("http://www.nytimes.com/2008/07/18/us/18cook.html?em&ex=1216526400&en=0fd5af153b22e24b&ei=5087%0A&_r=0") facing the 
Cook County Jail, the overcrowding problem is perhaps the most pressing; Cook County Jail has a limited supply of resources but very little control over its demand.
The jail has no control over the inflow of inmates from police arrests, and its ability to control the outflow of inmates is rather limited.
The main way in which CCJ frees up space is through a combination of electronic monitoring (by releasing certain inmates with ankle bracelets, for example) and probation.
The jail can relieve pressure on its resources by discharging certain inmates, but how do we know which inmates to release?

The solution: 
===
One way to determine which (groups of) inmates to release is to think about how the release of these inmates will impact crime in the city.
To do so strategically, the trick is to account for all of the city's underlying spatial and temporal trends.  Criminologists know that, in Chicago in particular, 
there are some particularly crime-ridden neighborhoods with much higher levels of violence than those of other neighborhoods.  And 
we also know that crime varies accross time; crime spikes on Fridays and during the summer because the weekend and warm weather attract
people outside and to the streets, where they are potential criminal targets.  Thus, we implemented a collection of spatiotemporal tests
to investigate how the release of inmates precedes subsequent crime trends with respect to both space and time.  This allowed us to identify
which groups of inmates are associated with later changes in criminal activity.  To assess the predictive capacity of these variables, a
predictive model is in the works.

The project:
===
There are three primary components to the project:

### Exploratory Data Analysis of Public Crime Data

Before we were able to begin predicting crime levels accross the city, we needed to gain an understanding of standard, baseline
levels of crime.  To do so, we conducted exploratory data anlaysis on data from the Chicago Data Portal.  In total, we examined about 
5.25 million crime reports spanning January 2001 through mid-2013.  For every reported criminal incident, 
these data document the incident’s category, location, date, time, and whether or not an arrest was made (more on the 
data below).  Given past knowledge about the crime in Chicago, we concentrated on spatial and temporal patterns.


### Implementation of Spatiotemporal Correlation Statistics

Once we began to understand historical trends in Chicago crime, we obtained data from the Cook County Jail on inmate
releases (more below).  Because the jail wants to free up space by releasing certain inmates, we decided to see how
crime levels change when groups of inmates (eg, violent vs. non-violent) are released from jail.  The Knox and Mantel 
tests were implemented, and the statistics generated from both of these test account for underying spatiotemporal trends.


### Predictive Model
After identifying significant spatiotemporal correlations, we decided to construct a predictive model to determine whether or not
these significant variables possess any predictive capacity.  This process is in the works.  

The data: Public Crime Data + Cook County Jail Data
===
The exploratory data analysis was conducted on the [Chicago Crime Portal Data]("https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-present/ijzp-q8t2#column-menu").
We restricted our analysis to data compiled through mid-2013.  For each crime report documented from the beginning of 2001 , these data contain the ID, case number, date, block, IUCR (Illinois Uniform Crime Reporting) code, type of crime (battery,
criminal assault, burglary, battery, vehicular theft, etc.) based on the corresponding IUCR code, a more detailed description, a
description of the incident's location (sidewalk, street, residential property, etc.), whether or not an arrest was made, whether or not
the incident was domestic, and its specific locaiton.  

The spatiotemporal metrics were calculated using the Cook County Jail Data.  These data include inmate's charges, self-reported
home address, booking/release dates, and some personal identifiers.  

## Installation Guide
git clone https://github.com/dssg/dssg-cpd-project
cd dssg-cpd-project

* Make sure PostgreSQL and other required software is installed, as described in the wiki.
* Check out the git repository and add dssg-cpd-project to your PYTHONPATH:
```
export PYTHONPATH=$PYTHONPATH:/path/to/dssg-cpd-project
```
* Run the SQL init scripts (`psql --host HOST --user USER DBNAME -f SCRIPT.sql`)
* Start analyzing data

Prerequisites
```
Git 
Python 2.7.3
```

From requirements.txt
```
Django==1.5.1
GDAL==1.9.1
GeoAlchemy2==0.2.1
SQLAlchemy==0.8.1
ipython==0.13.2
matplotlib==1.2.1
numpy==1.7.1
pandas==0.11.0
psycopg2==2.5
python-dateutil==2.1
pytz==2013b
scikit-learn==0.13.1
scipy==0.12.0
six==1.3.0
wsgiref==0.1.2
yolk==0.4.3
```

## Contributing to the Project
Issue Tracker
Email Addresses (good to use google group)
* Tom Plagge <tplagge@gmail.com>
* Varoon Bashyakarla <vbashyakarla@gmail.com>
* Ed McFowland <mcfowland@cmu.edu>
* Paul Meinshausen <meinshap@gmail.com>


License
===
Copyright (C) 2013 Data Science for Social Good Fellowship at the University of Chicago

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.




