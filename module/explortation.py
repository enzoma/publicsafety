#!/usr/bin/env python
import Tool
from knox import Knox
import numpy as np

one_sided_test = True
crime_comes_before = False 
areas = [ 'WEST SIDE', 'SOUTH SIDE', 'NORTH SIDE', 'NORTHWEST SIDE', 'LOOP', 'SOUTHWEST SIDE']
distance_cutoff = 5280.0/8.0
time_cutoffs = range(1,8)
time_cutoffs.extend([14, 21, 28, 35, 42, 49 ])
num_time_cutoffs = len(time_cutoffs)

graffiti={}
lights={}
buidlings={}
jail={}

for a in areas:
  '''
  d1 = Tool.load_data_from_db(\
    'SELECT x, y, ts '+\
    'FROM crime.crimes c join subareas s on st_contains(s.geom, c.geo) '+\
    'WHERE s.subarea_name=%s AND c.year=2012 AND c.ptype=%s', \
    'tplagge', 'tplagge', 'dssgpg',select_args=(a,'HOMICIDE',))
  '''

  # Load homicides from 2012
  d1 = Tool.load_data_from_db(\
    "SELECT x,y, ts " +\
    "FROM crime.crimes c join crime.subareas s on st_contains(s.geom, c.geo)" +\
    "WHERE c.year=2012 AND s.subarea_name=%s" +\
    "AND c.iucr IN ('0110','041A', '041B', '0420','0430','0440','0450','0451','0452','0453','0454','0460','0461','0462','0475','0479','0480','0481','0482','0483','0484','0485','0486','0487','0488','0489')", \
    'tplagge', 'tplagge', 'dssgpg', select_args=(a,))

  # Extract x, y, time
  x1, y1, t1 = d1['x'], d1['y'], d1['ts']



  ja = []
  graf = []
  light = []
  build = []
  for t in time_cutoffs:
    d2 = Tool.load_data_from_db(\
      'SELECT st_x(j.geo) as x, st_y(j.geo) as y, release_date ' +\
      'FROM jail.inmates_geocoded j join crime.subareas s on st_contains(s.geom, j.geo) ' +\
      'WHERE s.subarea_name=%s and extract(Year from release_date)=2012 ' +\
      'AND j.charge_code~%s', \
      'tplagge','tplagge','dssgpg', select_args=(a,'720 ILCS (550|570)',))
#      'tplagge','tplagge','dssgpg', select_args=(a,'720 ILCS 5[ /](12|24|19)',))

    # Extract x, y, time
    x2, y2, t2 = d2['x'], d2['y'], d2['release_date']
    print type(x2)

    if crime_comes_before:
      k = Knox(x1, y1, t1, x2, y2, t2)
    else:
      k = Knox(x2, y2, t2, x1, y1, t1)

    X,randdist = k.compute_test_statistic(distance_cutoff,t, one_sided_test)

    p_value = k.compute_p_value(X, randdist)
    print "Release v Crime (" + a + "): " + str(p_value)
    ja.append(p_value)
  

    d2 = Tool.load_data_from_db(\
      'SELECT st_x(j.geo) as x, st_y(j.geo) as y, release_date ' +\
      'FROM jail.inmates_geocoded j join crime.subareas s on st_contains(s.geom, j.geo) ' +\
      'WHERE s.subarea_name=%s and extract(Year from release_date)=2012 ' +\
      'AND j.charge_code~%s', \
      'tplagge','tplagge','dssgpg', select_args=(a,'720 ILCS (550|570)',))

    '''
    # Load graffiti reports from 2012
    d2 = Tool.load_data_from_db(\
      'SELECT x, y, casedate '+\
      'FROM threeoneone.graffiti t join crime.subareas s on st_contains(s.geom,t.) '+\
      'WHERE extract(Year from casedate)=%s', \
      'tplagge','tplagge','dssgpg',select_args=(2012,))

    # Extract x, y, time
    x2, y2, t2 = d2['x'], d2['y'], d2['casedate']
    if crime_comes_before:
      k = Knox(x1, y1, t1, x2, y2, t2)
    else:
      k = Knox(x2, y2, t2, x1, y1, t1)

    X,randdist = k.compute_test_statistic(distance_cutoff,t, one_sided_test)
    p_value = k.compute_p_value(X, randdist)
    print "Graffiti v Crime: " + str(p_value)
    graf.append(p_value)



    # Load Lights reports from 2012
    d2 = Tool.load_data_from_db(\
      'SELECT x, y, casedate FROM threeoneone.lights '+\
      'WHERE extract(Year from casedate)=%s', \
      'tplagge','tplagge','dssgpg',select_args=(2012,))

    x2, y2, t2 = d2['x'], d2['y'], d2['casedate']
    if one_sided_test & crime_comes_before:
      k = Knox(x1, y1, t1, x2, y2, t2)
    else:
      k = Knox(x2, y2, t2, x1, y1, t1)

    X,randdist = k.compute_test_statistic(5280.0/8.0,t, one_sided_test)
    p_value = k.compute_p_value(X, randdist)
    print "Lights v Crime: " + str(p_value)
    light.append(p_value)



    # Load vacant building reports from 2012
    d2 = Tool.load_data_from_db(\
      'SELECT x, y, servicedate FROM threeoneone.buildings '+\
      'WHERE extract(Year from servicedate)=%s', \
      'tplagge','tplagge','dssgpg',select_args=(2012,))

    x2, y2, t2 = d2['x'], d2['y'], d2['servicedate']

    if one_sided_test & crime_comes_before:
      k = Knox(x1, y1, t1, x2, y2, t2)
    else:
      k = Knox(x2, y2, t2, x1, y1, t1)

    X,randdist = k.compute_test_statistic(5280.0/8.0,t, one_sided_test)

    p_value = k.compute_p_value(X, randdist)
    print "Buildings v Crime: " + str(p_value)
    build.append(p_value)
    '''
  #graffiti[a] = graf
  #lights[a] = light
  #buildings[a] = build
  jail[a] = ja

