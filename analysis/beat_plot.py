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

  # This is a bear of an SQL query. It says:
  # 1. Count the violent crimes in beat 1914 by day.
  # 2. Make a list of all dates between 1/1/2001 and 1/30/2013.
  # 3. Join those two tables, setting the count to 0 if there are
  #    no violent crimes, or # of violent crimes otherwise.
  # 4. Order by date.
  select_sql = 'SELECT g::date date, COALESCE(c.count,0) ct FROM '+\
               '(SELECT ts::date date, count(*) FROM '+\
               ' crime.crimes WHERE current_beat=%s '+\
               ' AND isviolent=True GROUP BY ts::date) c '+\
               'RIGHT JOIN '+\
               'generate_series(%s, %s, interval %s) g '+\
               'ON g::date=c.date '+\
               'ORDER BY g::date'
  cur.execute(select_sql, (sys.argv[1], '2001-01-01', '2013-01-30', '1 day'))

  # Get all the rows in the response
  response = cur.fetchall()

  # Unpack them...
  dates_beat         = np.array([i[0] for i in response])
  violentcrimes_beat = np.array([i[1] for i in response])

  select_sql = 'SELECT g::date date, COALESCE(c.count,0) ct FROM '+\
               '(SELECT ts::date date, count(*) FROM '+\
               ' crime.crimes WHERE '+\
               ' isviolent=True GROUP BY ts::date) c '+\
               'RIGHT JOIN '+\
               'generate_series(%s, %s, interval %s) g '+\
               'ON g::date=c.date '+\
               'ORDER BY g::date'
  cur.execute(select_sql, ('2001-01-01', '2013-01-30', '1 day'))

  # Get all the rows in the response
  response = cur.fetchall()

  # Unpack them...
  dates         = np.array([i[0] for i in response])
  violentcrimes = np.array([i[1] for i in response])

  # And plot the smoothed results.
  smoothed_violentcrimes_beat = smooth(violentcrimes_beat,30)

  py.plot(dates[:-30],\
    violentcrimes[:-30]/float(np.mean(violentcrimes[0:100])),\
    'b-')
  py.plot(dates[:-30],\
    smoothed_violentcrimes_beat[:-30]/np.mean(smoothed_violentcrimes_beat[0:100]),\
    'r-')
  py.xlabel('Date')
  py.ylabel('Violent crimes')
  py.title('Violent crimes per day, normalized to January 2001')
  py.legend(['Citywide','Beat '+sys.argv[1]])
  py.savefig('violentcrimes_'+sys.argv[1]+'.png')
