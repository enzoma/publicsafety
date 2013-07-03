#!/bin/sh

USER=$(cat ../db_setup.cfg | grep DB_USER | awk -F: '{print $2}')
HOST=$(cat ../db_setup.cfg | grep DB_HOST | awk -F: '{print $2}')
NAME=$(cat ../db_setup.cfg | grep DB_NAME | awk -F: '{print $2}')

PSQL="psql --host $HOST --user $USER $NAME -f "

$PSQL create_crime_table.sql
./load_shapefiles.sh
$PSQL create_311_tables.sql
$PSQL create_censustract_table.sql
$PSQL create_censustract2000_table.sql
$PSQL create_iucr_table.sql
$PSQL create_weather_table.sql
$PSQL create_climate_table.sql
$PSQL supplement_crime_table.sql
