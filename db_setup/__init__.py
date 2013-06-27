import yaml
import os

DB_USER  = 'cpd'
DB_NAME  = 'cpd'
DB_HOST  = 'dssgpg'

setup_filename = 'db_setup.cfg'

config = {}

try:
  config = yaml.load(open(setup_filename,'r'))
except IOError:
  print('Local database config file (dbsetup.cfg) not found, assuming defaults.')

if 'DB_USER' in config.keys():
  DB_USER = config['DB_USER']
if 'DB_HOST' in config.keys():
  DB_HOST = config['DB_HOST']
if 'DB_NAME' in config.keys():
  DB_NAME = config['DB_NAME']
