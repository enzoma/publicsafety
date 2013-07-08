#!/usr/bin/env python

import db_setup
import psycopg2
import pandas.io.sql as sqlio

## Helper function to create (if necessary) a connection to the database
def get_db_conn(db_conn=None):
  if db_conn == None:
    # Make a connection to the database
    if db_setup.DB_PASSWORD == None:
      db_conn = psycopg2.connect(\
        database = db_setup.DB_NAME,\
        user     = db_setup.DB_USER,\
        host     = db_setup.DB_HOST)
    else:
      db_conn = psycopg2.connect(\
        database = db_setup.DB_NAME,\
        user     = db_setup.DB_USER,\
        host     = db_setup.DB_HOST,\
        password = db_setup.DB_PASSWORD)
  return db_conn

def mk_data_frame_from_sql_query(sql_query, db_conn=None):
  '''Fetches rows corresponding the provided sql query, places it
  into a data frame, and return the data frame'''
  # Create a dataframe that consists of the data defined by our SQL
  return sqlio.read_frame(sql_query, get_db_conn(db_conn))


