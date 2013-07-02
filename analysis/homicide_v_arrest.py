#!/usr/bin/env python

import db_setup
import psycopg2
import cPickle

# Make a connection to the database
conn = psycopg2.connect(\
  database = db_setup.DB_NAME,\
  user     = db_setup.DB_USER,\
  host     = db_setup.DB_HOST)

# Make a cursor to attach to the database
cur  = conn.cursor()

# Find the number of crimes per capita in each census tract from 2012
select_sql = 'SELECT t.tract, avg(t.pop), sum(c.arrest::integer), count(*) FROM census.c2010_tracts t JOIN '+\
             '(SELECT * FROM crime.crimes WHERE ptype=%s AND geo IS NOT NULL) c ON '+\
             'ST_Contains(t.geo, c.geo) GROUP BY t.tract'
cur.execute(select_sql,('HOMICIDE',))

# Fetch the results
out = cur.fetchall()
with open('/home/tplagge/tmp.pkl','wb') as f:
  cPickle.dump(out,f)
