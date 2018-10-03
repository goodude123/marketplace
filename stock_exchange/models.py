from django.utils import timezone
from django.db import models


# Create your models here.
class Currency(models.Model):
    name = models.CharField(max_length=30)
    unit = models.IntegerField(default=1)
    abbreviation = models.CharField(max_length=3)

    def __str__(self):
        return self.abbreviation


class Rate_and_date(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    rate = models.FloatField()
    date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.date = timezone.now()
        return super(Rate_and_date, self).save(*args, **kwargs)
