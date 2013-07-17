#!/usr/bin/env python
import Tool, knox
import cPickle

# Load homicides from 2012
d1 = Tool.load_data_from_db(\
  'SELECT x, y, ts FROM crime.crimes '+\
  'WHERE year=2012 AND ptype=%s', \
  'tplagge', 'tplagge', 'dssgpg',select_args=('HOMICIDE',))

# Load graffiti reports from 2012
d2 = Tool.load_data_from_db(\
  'SELECT x, y, casedate FROM threeoneone.graffiti '+\
  'WHERE extract(Year from casedate)=%s', \
  'tplagge','tplagge','dssgpg',select_args=(2012,))

# Extract x, y, time
x1, y1, t1 = d1['x'], d1['y'], d1['ts']
x2, y2, t2 = d2['x'], d2['y'], d2['casedate']

# Run the Knox test with characteristic distance = 1 mile
# and characteristic time = 30 days
X,randdist = knox.knox(x1,y1,t1,x2,y2,t2,5280.0/1.0,30.0)

# Save the output to a pickle file
with open('knox_example.pkl','wb') as f:
  cPickle.dump(X, f)
  cPickle.dump(randdist, f)

