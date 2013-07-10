#!/usr/bin/env python

# Import statements
import numpy as np
import csv
import collections
import time, datetime
import psycopg2

# Allow users to input csv files
# Data prereqs:
# 0) Must have column names without spaces
# 1) Must have lat/long coords
# 2) Must have timestamps (in some specific format)
# 3) Each variable must have a header

# First, query data from db or from csv to produce 
# a python (data) object.  As part of this, we identify
# the variable headers and populate the python (data) 
# object.

###############################################################################
# Helper functions for loading data
###############################################################################

def lists_to_arrays(data):
  '''Convert a dictionary of key: list to key: np.array'''
  for key, vallist in data.iteritems():
    # First find the numerical columns and switch any Nones or ''s
    # to np.nan's so the type gets set correctly.
    # This is a crazy trick to identify the numerical columns.
    # It uses the Counter histogramming routine on the types
    # of each variable in the list and identifies the most common
    # one.
    coltype = collections.Counter( \
      [type(i) for i in vallist if i is not None] ).most_common(1)
    if len(coltype) > 0: coltype = coltype[0][0]
    else:                coltype = None
    # If it's a numerical column, swap out the Nones and ''s for nans.
    if coltype == float or coltype == int:
      data[key] = [i if (i != None and i != '') else np.nan for i in vallist]
    # Now make the np.array.
    data[key] = np.array(data[key])
  return data


def auto_type_cast(d):
  ''' Helper function to guess at the data type of a string'''
  # If the input is not a string, then try to do something sensible.
  if not isinstance(d,str):
    if isinstance(d, collections.Iterable):
      # If we're passed a list, cast each list element.
      return [auto_type_cast(i) for i in d]
      # If we're passed any scalar other than a string, then just return it.
      return d

  # OK, we're dealing with a string.
  # First check for timestamp.
  # The data portal uses this:
  #   06/04/2013 05:00:00 AM
  try:    return time.strptime(d, '%m/%d/%Y %I:%M:%S %p')
  except: pass
  # Now check for date in m/d/y format.
  try:    return time.strptime(d, '%m/%d/%Y')
  except: pass
  # Now check for time alone in H:M:S am/pm format.
  # If the argument has an a.m. instead of am, the replace will fix it.
  try:    return time.strptime(d.replace('.',''),'%I:%M:%S %p')
  except: pass
  # Now check for time in 24-hour H:M:S format.
  try:    return time.strptime(d,'%H:%M:%S')
  except: pass
  # OK, we didn't get a timestamp we understand. Let's try an int.
  try:    return int(d)
  except: pass
  # OK, how about a float?
  try:    return float(d)
  except: pass
  # Must just be a plain ol' string.
  return d

###############################################################################
# CSV loader
###############################################################################

def load_data_from_csv(file_name):
  '''Read space and time stamped data from a CSV file.
     The file must have a header on the first line.'''
  # Open the file in a "with" block, which automatically
  # closes the file at the end.
  with open(file_name, 'rU') as f:
    # Parse it with the Python csv module.
    csvreader = csv.reader(f)
    # The first line should be a header.
    header = csvreader.next()

    # Initialize the data dictionary.
    # To make the header easier to use, make a hash
    # between column number and column name.
    data, columns = {}, {}
    for columnnum, columnname in enumerate(header):
      columns[columnnum] = columnname.lower()
      data[columnname.lower()]=[]

    # Loop over each row in the CSV file and fill the dictionary.
    for row in csvreader:
      for key, value in enumerate(row):
        data[columns[key]].append(auto_type_cast(value))

  data = lists_to_arrays(data)

  # Awesome. Return the result.
  return data

###############################################################################
# DB loader
###############################################################################

def load_data_from_db(select_string, db_name, db_user_name, db_host, \
                      db_user_passwd=None, select_args=()):
  '''Load data from a PostgreSQL database'''
  # Create a database connection
  conn = psycopg2.connect(\
    database = db_name,\
    user     = db_user_name,\
    password = db_user_passwd,\
    host     = db_host)
  # Get a cursor on the database
  cur = conn.cursor()
  # Issue the select command
  cur.execute(select_string, select_args)
  # Get the column information
  header = cur.description
  # Create a dictionary entry for each column
  data, columns = {}, {}
  for columnnum, columndesc in enumerate(header):
    data[columndesc.name.lower()] = []
    columns[columnnum] = columndesc.name.lower()
  # Loop through the columns and read them into the dictionary.
  for row in cur:
    for key, value in enumerate(row):
     if type(value) == datetime.datetime: 
       # Special case for timestamp columns.
       # Postgres returns a datetime, but we use timetuples for RPy.
       data[columns[key]].append(value.timetuple())
     else:
       data[columns[key]].append(value) 

  data = lists_to_arrays(data)

  # And return
  return data

###############################################################################
# Normalize space/time columns
###############################################################################

def normalize_space_time_columns(data):
  '''If we have long/lat data only, convert it to x/y in a projected SRID
     (by default, Chicago's, or 3435). If we have both a date and a time, conbine
     them into one datetime.'''
  # Space first. Simplify the labels.
  if 'x coordinate' in data.keys() and 'x' not in data.keys():
    data['x'] = data['x coordinate']
  if 'y coordinate' in data.keys() and 'y' not in data.keys():
    data['y'] = data['y coordinate']
  # Now make sure we have x and y.
  if 'x' not in data.keys() and 'y' not in data.keys():
    # If not, check for lat/long.

    if 'lat' in data.keys(): data['latitude']=data['lat']
    if 'lon' in data.keys(): data['longitude']=data['lon']
    if 'long' in data.keys(): data['longitude']=data['long']

    # OK, we have lat/long, so let's transform to X and Y.
    if 'latitude' in data.keys() \
      and 'longitude' in data.keys():
      # Use some magic from the OSGeo library to do the transform.
      from osgeo import ogr, osr
      srcSR=osr.SpatialReference()
      srcSR.SetWellKnownGeogCS('WGS84')
      destSR=osr.SpatialReference()
      destSR.ImportFromProj4("+proj=tmerc +lat_0=36.66666666666666 "+\
                             "+lon_0=-88.33333333333333 +k=0.9999749999999999 "+\
                             "+x_0=300000.0000000001 +y_0=0 +ellps=GRS80 "+\
                             "+towgs84=0,0,0,0,0,0,0 +units=us-ft +no_defs")
      ct=osr.CoordinateTransformation(srcSR,destSR)

      data['x'] = np.zeros(np.size(data['latitude']))
      data['y'] = np.zeros(np.size(data['latitude']))
      for i in range(np.size(data(['latitude']))):
        data['x'][i], data['y'][i], trash = \
        ct.TransformPoint(data['longitude'][i], data['latitude'][i])
    # TODO: normalize the time columns?
  return data




   
###############################################################################
  
# Obtain from user aggregation level of interest
# We can aggregate based on time intervals of interest,
# based on spatial boundaries, or based on features.
# Input = original dataset; output = dataset of interest
# based on user-obtained aggregation levels.


# Perform some exploratory data analysis. 
# Exploratory functions
# a) clustering labeled data in time 
# b) proportions of labeled data in user-defined areas
# c) in vs out
# d) in vs baseline 
# e) basic univariate visualizations




