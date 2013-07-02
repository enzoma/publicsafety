DSSG: Chicago Police Department
===
We are determining whether or not crime spikes when convicts return home after serving their sentences.

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
