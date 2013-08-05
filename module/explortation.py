#!/usr/bin/env python
import Tool
from knox import Knox
import numpy as np

# Load homicides from 2012
d1 = Tool.load_data_from_db(\
  'SELECT x, y, ts FROM crime.crimes '+\
  'WHERE year=2012 AND ptype=%s', \
  'tplagge', 'tplagge', 'dssgpg',select_args=('HOMICIDE',))

#d1 = Tool.load_data_from_db("select x,y, ts from crime.crimes where year=2012 and iucr in ('0110','041A', '041B', '0420','0430','0440','0450','0451','0452','0453','0454','0460','0461','0462','0475','0479','0480','0481','0482','0483','0484','0485','0486','0487','0488','0489')", 'tplagge', 'tplagge', 'dssgpg')

# Extract x, y, time
x1, y1, t1 = d1['x'], d1['y'], d1['ts']


time_cutoffs = range(1,8)
time_cutoffs.extend([14, 21, 28, 35, 42, 49 ])

num_time_cutoffs = len(time_cutoffs)
rel = []

'''
for t in time_cutoffs:
#  d2 = Tool.load_data_from_db(\
#    'select st_x(geo) as x, st_y(geo) as y, release_date from jail.inmates_geocoded where extract(Year from release_date)=2012',
#    'tplagge','tplagge','dssgpg')

  d2 = Tool.load_data_from_csv("/mnt/data1/CPD/jail/cleancrime.csv")

  # Extract x, y, time
  x2, y2, t2 = d2['x'], d2['y'], d2['release_date']


  k = Knox(x1, y1, t1, x2, y2, t2)
  X,randdist = k.compute_test_statistic(5280.0/8.0,t)

  p_value = k.compute_p_value(X, randdist)
  print "Release v Crime: " + str(p_value)
  rel.append(p_value)

print rel
'''
  

graf = []
light = []
build = []

for t in time_cutoffs:
  # Load graffiti reports from 2012
  d2 = Tool.load_data_from_db(\
    'SELECT x, y, casedate FROM threeoneone.graffiti '+\
    'WHERE extract(Year from casedate)=%s', \
    'tplagge','tplagge','dssgpg',select_args=(2012,))

  # Extract x, y, time
  x2, y2, t2 = d2['x'], d2['y'], d2['casedate']


  k = Knox(x1, y1, t1, x2, y2, t2)
  X,randdist = k.compute_test_statistic(5280.0/8.0,t)

  p_value = k.compute_p_value(X, randdist)
  print "Graffiti v Crime: " + str(p_value)
  graf.append(p_value)


'''
  # Load Lights reports from 2012
  d2 = Tool.load_data_from_db(\
    'SELECT x, y, casedate FROM threeoneone.lights '+\
    'WHERE extract(Year from casedate)=%s', \
    'tplagge','tplagge','dssgpg',select_args=(2012,))

  x2, y2, t2 = d2['x'], d2['y'], d2['casedate']
  k = Knox(x1, y1, t1, x2, y2, t2)
  X,randdist = k.compute_test_statistic(5280.0/8.0,t)

  p_value = k.compute_p_value(X, randdist)
  print "Lights v Crime: " + str(p_value)
  light.append(p_value)



  # Load vacant building reports from 2012
  d2 = Tool.load_data_from_db(\
    'SELECT x, y, servicedate FROM threeoneone.buildings '+\
    'WHERE extract(Year from servicedate)=%s', \
    'tplagge','tplagge','dssgpg',select_args=(2012,))

  x2, y2, t2 = d2['x'], d2['y'], d2['servicedate']
  k = Knox(x1, y1, t1, x2, y2, t2)
  X,randdist = k.compute_test_statistic(5280.0/8.0,t)

  p_value = k.compute_p_value(X, randdist)
  print "Buildings v Crime: " + str(p_value)
  build.append(p_value)
'''
