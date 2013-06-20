import os, csv, datetime
from django.contrib.gis.utils import LayerMapping
from models import PoliceBeat, Crime
from decimal import Decimal
from django.contrib.gis.geos import Point

#####################################################################
# For the beat shapefile, use the LayerMapping utility in geodjango.
#####################################################################

policebeat_mapping = {
  'district': 'DISTRICT',
  'sector'  : 'SECTOR',
  'beat'    : 'BEAT',
  'beat_num': 'BEAT_NUM',
  'geo'     : 'MULTIPOLYGON',
}

beat_shp = '/mnt/data1/CPD/policebeats/geo_aerh-rz74-1.shp'

def load_policebeat(verbose = True):
  lm = LayerMapping(PoliceBeat, beat_shp, policebeat_mapping,\
                    transform=False)
  lm.save(strict = True, verbose = verbose)

########################################################################
# For the crime data, use the csv reader to extract the relevant fields.
########################################################################

crimefile = '/mnt/data1/CPD/crimes_2013.csv'

def load_crimes(crimefile, verbose = False):
  with open(crimefile,'r') as f:
    reader = csv.reader(f)
    reader.next()

    for row in reader:
      crimeid   = row[0]
      caseno    = row[1]
      timestamp = datetime.datetime.strptime(row[2],'%m/%d/%Y %I:%M:%S %p')
      block     = row[3]
      iucr      = row[4]
      ptype     = row[5]
      desc      = row[6]
      locdesc   = row[7]
      arrest    = True if row[8]=='True' else False
      domestic  = True if row[9]=='True' else False
      beat_num  = int(row[10])
      district  = None if row[11]=='' else int(row[10])
      ward      = None if row[12]=='' else int(row[12])
      comm_area = None if row[13]=='' else int(row[13])
      fbi_code  = row[14]
      geo       = None if row[19]=='' else Point((Decimal(row[19]), Decimal(row[20])))

      try:
        # See if there is a duplicate crime in the database already.
        # If so, a new object doesn't need to be created.
        crime =  Crime.objects.get(\
          crimeid   = crimeid,\
          caseno    = caseno,\
          timestamp = timestamp,\
          block     = block,\
          iucr      = iucr,\
          ptype     = ptype,\
          desc      = desc,\
          locdesc   = locdesc,\
          arrest    = arrest,\
          domestic  = domestic,\
          beat_num  = beat_num,\
          district  = district,\
          ward      = ward,\
          comm_area = comm_area,\
          fbi_code  = fbi_code,\
          geo       = geo)
      except:
        # No previous crime matching this entry, so create a new one.
        crime =  Crime(\
          crimeid   = crimeid,\
          caseno    = caseno,\
          timestamp = timestamp,\
          block     = block,\
          iucr      = iucr,\
          ptype     = ptype,\
          desc      = desc,\
          locdesc   = locdesc,\
          arrest    = arrest,\
          domestic  = domestic,\
          beat_num  = beat_num,\
          district  = district,\
          ward      = ward,\
          comm_area = comm_area,\
          fbi_code  = fbi_code,\
          geo       = geo)

      crime.save()


def run(verbose = True):
  load_crimes(crimefile, verbose = verbose)
  load_policebeat(verbose = verbose)
