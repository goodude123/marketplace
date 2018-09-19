from django.db import models


# Create your models here.
class Currency(models.Model):
    name = models.CharField(max_length=30)
    unit = models.IntegerField(default=1)
    abbreviation = models.CharField(max_length=3)


class Rates_and_dates(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    rate = models.FloatField()
    date = models.DateTimeField('Course date')
