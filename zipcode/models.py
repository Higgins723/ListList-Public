from __future__ import unicode_literals

from django.contrib.gis.db import models

class Zipcode(models.Model):
    zipcode = models.CharField(max_length=5, null=True)
    affgeoid10 = models.CharField(max_length=14)
    census_bureau_codes = models.CharField(max_length=5)
    aland10 = models.FloatField()
    awater10 = models.FloatField()
    geom = models.MultiPolygonField(srid=4326)

    def __unicode__(self):
        return self.zipcode