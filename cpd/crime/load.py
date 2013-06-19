import os, csv, datetime
from django.contrib.gis.utils import LayerMapping
from models import PoliceBeat, Crime
from decimal import Decimal
from django.contrib.gis.geos import Point


policebeat_mapping = {
  'district': 'DISTRICT',
  'sector'  : 'SECTOR',
  'beat'    : 'BEAT',
  'beat_num': 'BEAT_NUM',
  'mpoly'   : 'MULTIPOLYGON',
}

beat_shp = '/mnt/data1/CPD/policebeats/geo_aerh-rz74-1.shp'

crimefile = '/mnt/data1/CPD/crimes_2013.csv'

def run(verbose = True):
  load_crimes(crimefile, verbose = verbose)
  load_policebeat(verbose = verbose)

def load_policebeat(verbose = True):
  lm = LayerMapping(PoliceBeat, beat_shp, policebeat_mapping,\
                    transform=False)
  lm.save(strict = True, verbose = verbose)

def load_crimes(crimefile, verbose = False):
  with open(crimefile,'r') as f:
    reader = csv.reader(f)
    reader.next()
    for row in reader:
      try:
        crime =  Crime.objects.get(\
        crimeid   = row[0],\
        caseno    = row[1],\
        timestamp = datetime.datetime.strptime(row[2],'%m/%d/%Y %I:%M:%S %p'),\
        block     = row[3],\
        iucr      = row[4],\
        ptype     = row[5],\
        desc      = row[6],\
        locdesc   = row[7],\
        arrest    = True if row[8]=='True' else False,\
        domestic  = True if row[9]=='True' else False,\
        beat      = int(row[10]),\
        district  = None if row[11]=='' else int(row[10]),\
        ward      = int(row[12]),\
        comm_area = int(row[13]),\
        loc       = None if row[19]=='' else Point((Decimal(row[19]), Decimal(row[20]))))
      except:
        crime =  Crime(\
        crimeid   = row[0],\
        caseno    = row[1],\
        timestamp = datetime.datetime.strptime(row[2],'%m/%d/%Y %I:%M:%S %p'),\
        block     = row[3],\
        iucr      = row[4],\
        ptype     = row[5],\
        desc      = row[6],\
        locdesc   = row[7],\
        arrest    = True if row[8]=='True' else False,\
        domestic  = True if row[9]=='True' else False,\
        beat      = int(row[10]),\
        district  = None if row[11]=='' else int(row[10]),\
        ward      = int(row[12]),\
        comm_area = int(row[13]),\
        loc       = None if row[19]=='' else Point((Decimal(row[19]), Decimal(row[20]))))


      crime.save()
