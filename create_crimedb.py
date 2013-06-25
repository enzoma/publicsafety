#!/usr/bin/env python
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy
from sqlalchemy import Column, Integer, String, DateTime, Boolean, MetaData, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref
from geoalchemy2 import Geometry
import geoalchemy2.functions as func
from osgeo import gdal, ogr, osr
import csv, datetime, sys
from crimedb_orm import PoliceBeat, Crime

# Create a database connection engine and 
# build an appropriate base class from it.
engine   = sqlalchemy.create_engine('postgres://cpd@dssgpg/cpd')
metadata = MetaData(engine)
Base     = declarative_base(metadata=metadata)
Session  = sessionmaker(bind=engine)

################################################################################################

def drop_tables():
  metadata.drop_all(engine)

################################################################################################

def create_policebeat_table(shapefile='/mnt/data1/CPD/policebeats.longlat/geo_aerh-rz74-1.shp'):
  PoliceBeat.__table__.create(engine)

  # Create the coordinate transform from long/lat to projection 3435.
  srcSR  = osr.SpatialReference()
  srcSR.SetWellKnownGeogCS('WGS84')
  destSR = osr.SpatialReference()
  destSR.ImportFromEPSG(3435)
  ct=osr.CoordinateTransformation(srcSR,destSR)

  # Open the shapefile.
  shpfile = ogr.Open(shapefile)
  layer   = shpfile.GetLayer(0)

  # Loop through each entry in the shapefile and create a new PoliceBeat object.
  session = Session()
  for i in range(layer.GetFeatureCount()):
    f        = layer.GetFeature(i)
    beat_num = f.GetFieldAsInteger('BEAT_NUM')
    district = f.GetFieldAsInteger('DISTRICT')
    sector   = f.GetFieldAsInteger('SECTOR')
    beat     = f.GetFieldAsInteger('BEAT')
    geo      = f.GetGeometryRef().Clone()
    geo.Transform(ct)
    geo_wkt  = 'SRID=3435;'+geo.ExportToWkt()
    pb = PoliceBeat(district,sector,beat,beat_num,geo_wkt)
    # Norridge and Harwood Heights (separate cities surrounded by Chicago)
    # are encoded as district 31. They aren't actually any CPD district.
    # So, skip them.
    if district == 31: continue

    # Add the object to the session.
    session.add(pb)

  # Commit all the beats!
  session.commit()

################################################################################################

def create_crime_table(crimefile='/mnt/data1/CPD/crimes_2013.csv'):
  try:
    Crime.__table__.drop(engine)
  except:
    pass
  Crime.__table__.create(engine)

  # Create the coordinate transform from long/lat to projection 3435.
  srcSR  = osr.SpatialReference()
  srcSR.SetWellKnownGeogCS('WGS84')
  destSR = osr.SpatialReference()
  destSR.ImportFromEPSG(3435)
  ct=osr.CoordinateTransformation(srcSR,destSR)

  with open(crimefile, 'r') as f:
    reader = csv.reader(f)
    reader.next()

    session = Session()
    for irow,row in enumerate(reader):
      if (irow % 10000 == 0): print irow
      crimeid   = row[0]
      caseno    = row[1]
      timestamp = datetime.datetime.strptime(row[2],'%m/%d/%Y %I:%M:%S %p')
      block     = row[3]
      iucr      = row[4]
      ptype     = row[5]
      desc      = row[6]
      locdesc   = row[7]
      arrest    = True if row[8].lower()=='true' else False
      domestic  = True if row[9].lower()=='true' else False
      portal_beat = int(row[10])
      district  = None if row[11]=='' else int(row[10])
      ward      = None if row[12]=='' else int(row[12])
      comm_area = None if row[13]=='' else int(row[13])
      fbi_code  = row[14]
      geo_wkt   = None
      if row[19] != '':
        long  = float(row[20])
        lat   = float(row[19])
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(long,lat)
        point.Transform(ct)
        point.FlattenTo2D()
        geo_wkt  = 'SRID=3435;'+point.ExportToWkt()
      beat_num   = None
      if geo_wkt != None:
        try:
          beat_num = session.query(PoliceBeat.beat_num).\
            filter(func.ST_Contains(PoliceBeat.geo, geo_wkt)).one()
        except:
          beat_num = None
      c = Crime(crimeid,caseno,timestamp,block,iucr,ptype,\
                desc,locdesc,arrest,domestic,portal_beat,district,ward,comm_area,\
                fbi_code,beat_num,geo_wkt)
      session.add(c)

  # Commit all the beats!
  session.commit()


if __name__=='__main__':
  #drop_tables()
  #create_policebeat_table()
  #create_crime_table()
  pass
