DSSG: Crime and Incarceration
===
This is a (Data Science for Social Good)["http://www.dssg.io/"] project to develop a series of methods to detect spatio-temporal correlations between point-processes and to model the relationships between them. This project is specifically concerned with criminal activity and incarceration and release processes in the city of Chicago. Our driving question is whether we can use the release of jail inmates to predict changes in crime in Chicago. 

The problem: 
===
Current police analyses primarily rely on crime report data collected by the police department itself. Predictive analysis could be improved by incorporating additional data, especially data from other government organizations within the criminal justice sector. Our goal is to see whether jail releases and 311 complaints are leading indicators of violent crime. These new predictors will be used by the Chicago Police Department to improve their models and to help officers get ahead of violence.

The solution: 
===

The project:
===

The data:
===

License
===
Copyright (C) 2013 Data Science for Social Good Fellowship at the University of Chicago

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Instructions
===
* Make sure PostgreSQL and other required software is installed, as described in the wiki.
* Check out the git repository and add dssg-cpd-project to your PYTHONPATH:
```
export PYTHONPATH=$PYTHONPATH:/path/to/dssg-cpd-project
```
* Run the SQL init scripts (`psql --host HOST --user USER DBNAME -f SCRIPT.sql`)
* Start analyzing data


Motivation
===
Crime persists as a serious problem in Chicago.  As of April 2013, $31.9 million of the total $38 million city
budget to pay for overtime police had been depleted, and 2012 was a particularly deadly year with over 500 homicides.
The CPD employs predictive spatial-temporal models and social network analysis to preempt crime but have often
arrested inviduals with criminal history records, some of which are rather extensive.  As a result, we grew interested
in determining whether or not crime spikes when prisoners return home upon completing their prison sentences.  

This is a particularly interesting question for two primary reasons.  First, the CPD has not yet studied associations
between arrests, prison sentences, and potential crime spikes.  Secondly, if such an association exists, this
analysis can be used to foster dialogues between law enforcement and criminal justice efforts to refine sentences
and incentives in order to mitigate and, ultimatley, to prevent crime.

Installation
===
git clone https://github.com/dssg/dssg-cpd-project
cd dssg-cpd-project

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

Contact Us
===
* Tom Plagge <tplagge@gmail.com>
* Varoon Bashyakarla <vbashyakarla@gmail.com>
* Ed McFowland <mcfowland@cmu.edu>
* Paul Meinshausen <meinshap@gmail.com>
