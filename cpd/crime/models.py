from django.contrib.gis.db import models

class PoliceBeat(models.Model):
  district = models.IntegerField('District')
  sector   = models.IntegerField('Sector')
  beat     = models.IntegerField('Beat')
  beat_num = models.IntegerField('Beat number')

  mpoly    = models.MultiPolygonField()
  objects  = models.GeoManager()

  def __unicode__(self):
    return self.beat_num

class Crime(models.Model):
  crimeid   = models.CharField('ID', max_length=20)
  caseno    = models.CharField('Case Number', max_length=20)
  timestamp = models.DateTimeField('Timestamp')
  block     = models.CharField('Block', max_length=60)
  iucr      = models.CharField('IUCR',max_length=10)
  ptype     = models.CharField('Primary Type', max_length=100)
  desc      = models.CharField('Description', max_length=100)
  locdesc   = models.CharField('Location Description', max_length=100)
  arrest    = models.BooleanField('Arrest')
  domestic  = models.BooleanField('Domestic')
  beat      = models.IntegerField('Beat number')
  district  = models.IntegerField('District',null=True)
  ward      = models.IntegerField('Ward')
  comm_area = models.IntegerField('Community Area')
  
  loc       = models.PointField(null=True)
  objects   = models.GeoManager()

  def __unicode__(self):
    return self.crimeid
  
