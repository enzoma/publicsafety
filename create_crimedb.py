#!/usr/bin/env python
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy
from sqlalchemy import Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker
from geoalchemy2 import Geometry
from osgeo import gdal, ogr, osr

# Create a database connection engine and 
# build an appropriate base class from it.
engine   = sqlalchemy.create_engine('postgres://cpd@dssgpg/cpd')
metadata = MetaData(engine)
Base     = declarative_base(metadata=metadata)
Session  = sessionmaker(bind=engine)

# Create a representation of a police beat.
class PoliceBeat(Base):
  __tablename__ = 'beats'
  district = Column(Integer)
  sector   = Column(Integer)
  beat     = Column(Integer)
  beat_num = Column(Integer, primary_key=True)
  geo      = Column(Geometry('POLYGON',dimension=2,srid=3435))

  def __init__(self,district,sector,beat,beat_num,geo):
    self.district, self.sector = district, sector
    self.beat, self.beat_num   = beat, beat_num
    self.geo                   = geo


def create_policebeat_table(shapefile='/mnt/data1/CPD/policebeats.longlat/geo_aerh-rz74-1.shp'):
  # Create the table. If it already exists, drop it first.
  try:
    PoliceBeat.__table__.drop(engine)
  except:
    pass
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

if __name__=='__main__':
  create_policebeat_table()

