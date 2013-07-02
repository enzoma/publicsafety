#!/usr/bin/env python

import db_setup
import psycopg2

# Make a connection to the database
conn = psycopg2.connect(\
  database = db_setup.DB_NAME,\
  user     = db_setup.DB_USER,\
  host     = db_setup.DB_HOST)

# Make a cursor to attach to the database
cur  = conn.cursor()

# Find the number of crimes per capita in each census tract from 2012
select_sql = 'SELECT t.tract, avg(t.pop), count(*) FROM census.c2010_tracts t JOIN '+\
             '(SELECT * FROM crime.crimes WHERE geo IS NOT NULL AND year=2012) c ON '+\
             'ST_Contains(t.geo, c.geo) GROUP BY t.tract'
cur.execute(select_sql)

# Fetch the results
out = cur.fetchall()
# Sort them by per capita crime and print.
for tract, pop, count in sorted(out, key = lambda i: i[2]/i[1] if i[1]!=0 else None):
  print '%12d %8.3f' % (tract, count/pop if pop!=0 else 0)

SELECT j.neighborhood, n.geo, j.ct, j.ct/ST_Area(n.geo) FROM
  (SELECT n.pri_neigh neighborhood, count(*) ct FROM
   neighborhoods n JOIN crimes c ON ST_Contains(n.geom, c.geo)
   WHERE c.year=2012 AND c.geo IS NOT NULL) j JOIN 
   neighborhoods n ON j.neighborhood=n.neighborhood;
