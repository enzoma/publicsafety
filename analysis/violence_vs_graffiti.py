#!/usr/bin/env python

# Given a beat number as a command line argument, plot the 30 day moving average
# of the number of violent crimes.

import numpy as np
import pylab as py
import psycopg2
import aggregates as a
import sys

def smooth(vec, N):
  # Take an N-day moving average
  # Convolution is the fastest way to do this.
  return np.convolve(vec, np.ones((N,))/float(N))[(N-1):]

## If called directly, print an example.
if __name__=='__main__':

  # Get a psycopg2 cursor using the function in aggregates.py
  cur = a.get_cursor()

  select_sql = 'SELECT g::date date, COALESCE(c.count,0) ct FROM '+\
               '(SELECT ts::date date, count(*) FROM '+\
               ' crime.crimes WHERE current_beat=%s '+\
               ' AND isviolent=True GROUP BY ts::date) c '+\
               'RIGHT JOIN '+\
               'generate_series(%s, %s, interval %s) g '+\
               'ON g::date=c.date '+\
               'ORDER BY g::date'
  cur.execute(select_sql, (sys.argv[1], '2012-01-01', '2013-01-30', '1 day'))

  # Get all the rows in the response
  response = cur.fetchall()

  # Unpack them...
  dates_beat         = np.array([i[0] for i in response])
  violentcrimes_beat = np.array([i[1] for i in response])

  # And plot the smoothed results.
  smoothed_violentcrimes_beat = smooth(violentcrimes_beat,30)

  select_sql = 'SELECT g::date date, COALESCE(c.count,0) ct FROM '+\
               '(SELECT casedate::date date, count(*) FROM '+\
               ' threeoneone.graffiti WHERE current_beat=%s '+\
               ' GROUP BY casedate::date) c '+\
               'RIGHT JOIN '+\
               'generate_series(%s, %s, interval %s) g '+\
               'ON g::date=c.date '+\
               'ORDER BY g::date'
  cur.execute(select_sql, (sys.argv[1], '2012-01-01', '2013-01-30', '1 day'))

  # Get all the rows in the response
  response = cur.fetchall()

  # Unpack them...
  dates             = np.array([i[0] for i in response])
  graffitis_beat     = np.array([i[1] for i in response])

  # And plot the smoothed results.
  smoothed_graffitis_beat     = smooth(graffitis_beat, 30)

  py.plot(dates[:-30],\
    smoothed_violentcrimes_beat[:-30],\
    'b-')
  py.plot(dates[:-30],\
    smoothed_graffitis_beat[:-30],\
    'r-')
  py.xlabel('Date')
  py.ylabel('Count')
  py.title('Violent crimes / graffitis per day, normalized to January 2012, beat '+sys.argv[1])
  py.legend(['Violent crime','Graffiti report'])
  py.savefig('graffiti_'+sys.argv[1]+'.png')
