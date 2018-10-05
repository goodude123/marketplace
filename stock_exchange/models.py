from django.db import models


# Create your models here.
class Currency(models.Model):
    name = models.CharField(max_length=30)
    unit = models.IntegerField(default=1)
    code = models.CharField(max_length=3)

    def __str__(self):
        return self.code


class Rate_and_date(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    rate = models.FloatField()
    date = models.DateTimeField()

    def __str__(self):
        return self.currency.code + ' ' + self.date.strftime('%Y-%m-%d')
