#!/usr/bin/env python
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy
from sqlalchemy import Column, Integer, String, DateTime, Boolean, MetaData, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref
from geoalchemy2 import Geometry
import geoalchemy2.functions as func
from osgeo import gdal, ogr, osr
import csv, datetime, sys

# Create a database connection engine and 
# build an appropriate base class from it.
engine   = sqlalchemy.create_engine('postgres://cpd@dssgpg/cpd')
metadata = MetaData(engine)
Base     = declarative_base(metadata=metadata)

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

class Crime(Base):
  __tablename__ = 'crime'
  id          = Column(Integer, primary_key=True)
  crimeid     = Column(String)
  caseno      = Column(String)
  timestamp   = Column(DateTime)
  block       = Column(String)
  iucr        = Column(String)
  ptype       = Column(String)
  desc        = Column(String)
  locdesc     = Column(String)
  arrest      = Column(Boolean)
  domestic    = Column(Boolean)
  portal_beat = Column(Integer)
  district    = Column(Integer)
  ward        = Column(Integer)
  comm_area   = Column(Integer)
  fbi_code    = Column(String)
  beat_num    = Column(Integer,ForeignKey('beats.beat_num'))
  geo         = Column(Geometry('POINT',dimension=2,srid=3435))

  beat        = relationship('PoliceBeat', backref=backref('crimes', order_by=id))

  def __init__(self, crimeid, caseno, timestamp, block, iucr, \
               ptype, desc, locdesc, arrest, domestic, portal_beat, \
               district, ward, comm_area, fbi_code, beat_num, geo):
    self.crimeid, self.caseno, self.timestamp = crimeid, caseno, timestamp
    self.block, self.iucr, self.ptype = block, iucr, ptype
    self.desc, self.locdesc, self.arrest = desc, locdesc, arrest
    self.domestic, self.portal_beat, self.district = domestic, portal_beat, district
    self.ward, self.comm_area, self.fbi_code = ward, comm_area, fbi_code
    self.beat_num, self.geo = beat_num, geo
