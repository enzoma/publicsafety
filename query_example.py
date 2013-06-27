#!/usr/bin/env python

import db_setup
import psycopg2

conn = psycopg2.connect(\
  database = db_setup.DB_NAME,\
  user     = db_setup.DB_USER,\
  host     = db_setup.DB_HOST)

cur  = conn.cursor()

select_sql = 'SELECT t.tract, avg(t.pop), count(*) FROM census.c2010_tracts t JOIN (SELECT * FROM crime.crimes WHERE geo IS NOT NULL AND year=2012) c ON '+\
             'ST_Contains(t.geo, c.geo) GROUP BY t.tract'

cur.execute(select_sql)
out = cur.fetchall()
for tract, pop, count in sorted(out, key = lambda i: i[2]/i[1] if i[1]!=0 else None):
  print '%12d %8.3f' % (tract, count/pop if pop!=0 else 0)
