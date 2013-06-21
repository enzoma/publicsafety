from django.contrib.gis.db import models

class PoliceBeat(models.Model):
  district = models.IntegerField('District')
  sector   = models.IntegerField('Sector')
  beat     = models.IntegerField('Beat')
  beat_num = models.IntegerField('Beat number')

  geo      = models.PolygonField(srid=3435)
  objects  = models.GeoManager()

  def __unicode__(self):
    return str(self.beat_num)

class CensusTract(models.Model):
  tractid  = models.CharField('FIPS code', max_length=11)
  geo      = models.MultiPolygonField(srid=3435)
  objects  = models.GeoManager()

  def __unicode__(self):
    return str(self.tractid)

class CensusBlock(models.Model):
  geoid    = models.CharField('FIPS code', max_length=15)
  geo      = models.MultiPolygonField(srid=3435)
  objects  = models.GeoManager()

  def __unicode__(self):
    return str(self.geoid)

class Crime(models.Model):
  crimeid     = models.CharField('ID', max_length=20)
  caseno      = models.CharField('Case Number', max_length=20)
  timestamp   = models.DateTimeField('Timestamp')
  block       = models.CharField('Block', max_length=60)
  iucr        = models.CharField('IUCR',max_length=10)
  ptype       = models.CharField('Primary Type', max_length=100)
  desc        = models.CharField('Description', max_length=100)
  locdesc     = models.CharField('Location Description', max_length=100)
  arrest      = models.BooleanField('Arrest')
  domestic    = models.BooleanField('Domestic')
  beat_num    = models.IntegerField('Beat number')
  district    = models.IntegerField('District',null=True)
  ward        = models.IntegerField('Ward',null=True)
  comm_area   = models.IntegerField('Community Area',null=True)
  fbi_code    = models.CharField('FBI code',max_length=20)
  beat        = models.ForeignKey(PoliceBeat,null=True)
  censustract = models.ForeignKey(CensusTract,null=True)
  #censusblock = models.ForeignKey(CensusBlock)
  
  geo       = models.PointField(null=True,srid=3435)
  objects   = models.GeoManager()

  def __unicode__(self):
    return self.crimeid
  
