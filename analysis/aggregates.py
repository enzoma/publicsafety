#!/usr/bin/env python
import psycopg2
import db_setup
import datetime

## Helper functions for dealing with datetime.dates
def dayofyear_from_date(date):
  '''Get the day of the year (1-366) from a datetime.date object.'''
  return int(date.strftime('%j'))

def dayofweek_from_date(date):
  '''Get the day of the week (0-6) from a datetime.date ojbect.'''
  return date.weekday()

## Helper function for dealing with psycopg2 cursors
def get_cursor(cur=None):
  if cur==None:
    conn = psycopg2.connect(\
      database = db_setup.DB_NAME,\
      user     = db_setup.DB_USER,\
      host     = db_setup.DB_HOST)
    cur = conn.cursor()
  return cur

## Helper function for police beats
def get_beats(cur=None):
  '''Get a list of all the beats in the city.'''
  cur = get_cursor(cur)
  cur.execute('SELECT beat_num FROM crime.cpdbeats')
  return cur.fetchall()

## Functions for querying the crimes table
def get_crime_iterator(where_clause, args=None, cur=None):
  '''Fetch rows from crimes table based on some where clause.
  If there is an argument tuple to pass to the execute command,
  it can be optionally included.  Return an iterator.'''
  
  cur = get_cursor(cur)

  select_sql = 'SELECT * FROM crime.crimes WHERE '+where_clause
  if args == None:
    cur.execute(select_sql)
  else: 
    cur.execute(select_sql,args)
  return cur 


def crime_by_beat_and_date(beat_num, date=None, 
  violent=None, index=None, cur=None):
  '''Fetch all crimes from a given beat number, and a given
  date or dates.  Return a list of rows.
  If violent/index is None, don't select based on those.
  If True or False, then do.
  beat_num can be either a string ('0123') or an integer (123).
  date can be either a string ('1/31/2001') or a datetime.date.'''

  cur = get_cursor(cur)

  if type(beat_num) == type(1):
    beat_num = '%04d' % beat_num
  if type(date) == type(datetime.date(2001,1,31)): 
    date = '%d/%d/%d' % (date.month,date.day,date.year)

  pre_query = ''
  if violent != None:
    if violent: pre_query = pre_query + 'isviolent=True  AND '
    else:       pre_query = pre_query + 'isviolent=False AND '
  if index != None:
    if index:   pre_query = pre_query + 'isindex=True  AND '
    else:       pre_query = pre_query + 'isindex=False AND '

  return get_crime_iterator(pre_query + 'current_beat = %s AND date(ts) = %s', \
    args=(beat_num, date), cur=cur).fetchall()

## If called directly, print an example.
if __name__=='__main__':
  print crime_by_beat_and_date(1914, '1/31/2001', violent=True)
