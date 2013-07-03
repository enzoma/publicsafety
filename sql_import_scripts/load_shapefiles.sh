#!/bin/sh

USER=$(cat ../db_setup.cfg | grep DB_USER | awk -F: '{print $2}')
HOST=$(cat ../db_setup.cfg | grep DB_HOST | awk -F: '{print $2}')
NAME=$(cat ../db_setup.cfg | grep DB_NAME | awk -F: '{print $2}')

shp2pgsql -I -s 3435 /mnt/data1/CPD/Shapefiles/cpd_beats/cpd_beats.shp CPDBeats | psql --host $HOST --user $USER $NAME
shp2pgsql -I -s 3435 /mnt/data1/CPD/Shapefiles/School_20Grounds/School_Grounds.shp SchoolGrounds | psql --host $HOST --user $USER $NAME
shp2pgsql -I -s 3435 /mnt/data1/CPD/Shapefiles/cpd_districts/cpd_districts.shp CPDDistricts | psql --host $HOST --user $USER $NAME
shp2pgsql -I -s 3435 /mnt/data1/CPD/Shapefiles/cpd_sectors/cpd_sectors.shp CPDSectors | psql --host $HOST --user $USER $NAME
shp2pgsql -I -s 3435 /mnt/data1/CPD/Shapefiles/Comm_20Areas/CommAreas.shp CommAreas | psql --host $HOST --user $USER $NAME
shp2pgsql -I -s 3435 /mnt/data1/CPD/Shapefiles/Wards/Wards.shp wards | psql --host $HOST --user $USER $NAME
shp2pgsql -I -s 3435 /mnt/data1/CPD/Shapefiles/cpd_stations/cpd_stations.shp CPDStations | psql --host $HOST --user $USER $NAME
shp2pgsql -I -s 3435 /mnt/data1/CPD/Shapefiles/Hospitals/Hospitals.shp Hospitals | psql --host $HOST --user $USER $NAME

