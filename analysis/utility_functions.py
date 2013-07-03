#!/usr/bin/env python

import db_setup
import psycopg2
import pandas.io.sql as sqlio

def mk_data_frame_from_sql_query(sql_query, db_conn=None):

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

  # Create a dataframe that consists of the data defined by our SQL
  return(sqlio.read_frame(sql_query, db_conn))
