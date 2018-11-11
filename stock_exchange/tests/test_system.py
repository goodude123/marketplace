from django.test import TestCase
from django.utils import timezone
from ..models import Currency
from ..system import pack


class TestPackModule(TestCase):
    def setUp(self):
        currency = Currency(name='dolar', code='USD', unit=1)
        currency.save()
        currency.rate_and_date_set.create(rate=3.60, date="2011-09-01 11:20:30+00:00")

    def test_valid_get_last_rate(self):
        currency = Currency.objects.get(code='USD')
        last_rate_returned_by_function = pack.get_last_rate(currency)
        last_rate = currency.rate_and_date_set.all().latest('date').rate

        self.assertEqual(last_rate_returned_by_function, last_rate)

    def test_valid_get_last_date(self):
        currency = Currency.objects.get(code='USD')
        last_date_returned_by_function = pack.get_last_date(currency)
        last_date = "2011-09-01 11:20:30+00:00"

        self.assertEqual(str(last_date_returned_by_function), last_date)
