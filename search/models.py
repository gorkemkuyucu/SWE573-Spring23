from django.db import models

# Create your models here.

from django.contrib.gis.db import models


class MarkedPoint(models.Model):
    location = models.PointField()