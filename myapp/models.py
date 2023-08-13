from django.db import models

# Create your models here.
class dim(models.Model):
    wid=models.FloatField()
    ht=models.FloatField()
    img=models.CharField(max_length=100)

class ptp(models.Model):
    dist=models.IntegerField()
    img=models.CharField(max_length=100)
