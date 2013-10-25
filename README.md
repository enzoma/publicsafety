DSSG: Public Safety
===
This is a [Data Science for Social Good]("http://www.dssg.io/") project to assess the correlation of spatio-temporal
point processes with violent crime. This code was used in projects with the Chicago Police Department and 
the Cook County Sheriff's Office. Some of the point processes we explored included jail releases and 311 complaints.

===

The problem
===
While violent crime in Chicago has broadly declined since the turn of the century, the decline has not kept pace with
other cities such as New York and Los Angeles. As a result, both the Police Department and the Cook County Sheriff's
Office (the agency in charge of operating the county jail) remain resource-constrained. The DSSG fellows worked on projects
with both agencies to seek out new leading indicators of violence, with the hope of giving police officers an extra edge, and
helping the jail identify high-risk individuals.

In both cases, the methodological strategy for identifying leading indicators was the same: use violent crime reports
from the Chicago public data portal as a proxy for violence, and seek out other point processes that are leading indicators
of violence.

Criminologists know that, in Chicago in particular, 
there are some particularly crime-ridden neighborhoods with much higher levels of violence than those of other neighborhoods.  And 
we also know that crime varies accross time; crime spikes on Fridays and during the summer because the weekend and warm weather attract
people outside and to the streets, where they are potential criminal targets.  Thus, we implemented a collection of spatiotemporal tests
to investigate how the release of inmates precedes subsequent crime trends with respect to both space and time.  This allowed us to identify
which groups of inmates are associated with later changes in criminal activity.  To assess the predictive capacity of these variables, a
predictive model is in the works.

The project
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
releases (more below).  Because the jail may be able to free up space by releasing certain inmates, we decided to see how
crime levels change when groups of inmates (e.g., violent vs. non-violent) are released from jail.  The Knox and Mantel 
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

### Installation Guide
git clone https://github.com/dssg/publicsafety
cd publicsafety

* Make sure PostgreSQL and other required software is installed, as described in the wiki.
* Check out the git repository and add dssg/publicsafety to your PYTHONPATH:
```
export PYTHONPATH=$PYTHONPATH:/path/to/dssg/publicsafety
```
* Run the SQL init scripts (`psql --host HOST --user USER DBNAME -f SCRIPT.sql`)
* Start analyzing data

Prerequisites
```
Git
PostgreSQL with PostGIS
Python 2.7.3
```

See also requirements.txt.

### Repository layout
`analysis/`: Exploratory data analysis tools.
`data_preparation/`: Data cleaning scripts.
`db_setup/`: Helper module for managing database communications.
`publicsafety/`: Spatio-temporal correlation tests.
`sql_import_scripts/`: Scripts for loading data into the PostgreSQL database.
`util/`: General helper functions for parsing and manipulating and using census and weather data, etc.
`visualizations/`: Data visualizations we found useful to keep around.
`predictive_model/`: Regression analysis for crime data. Not yet committed.


## Contributing to the Project
If you're interested in getting involved, please check out the [issue tracker]("https://github.com/dssg/publicsafety/issues?state=open")

To get in touch, please email a team member.  
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




