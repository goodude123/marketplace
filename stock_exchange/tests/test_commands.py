from django.utils import timezone
from django.test import TestCase
from ..management.commands import _currency as currency
from ..management.commands import _save
from ..models import Currency



class SetUp(TestCase):
    def setUp(self):
        currency = Currency(name='dolar', code='USD', unit=1)
        currency.save()

class CurrencyTestCase(TestCase):
    def test_valid_create_currency(self):
        currency_object = currency.SingleCurrency(
            name='dolar',
            unit=1,
            code='USD',
            rate=3.29,
            date="2011-09-01T13:20:30"
        )

    def test_invalid_create_currency(self):
        with self.assertRaises(TypeError):
            currency_object = currency.SingleCurrency()


class SaveFunctionTestCase(SetUp):
    def test_valid_save_new_rate_and_date(self):
        currency = Currency.objects.get(name='dolar')
        rate = 3.29
        date = "2011-09-01 11:20:30+00:00"
        _save.save_new_rate_and_date(currency, [rate, date])
        new_rate = currency.rate_and_date_set.order_by('-date')[0].rate
        new_date = currency.rate_and_date_set.order_by('-date')[0].date
        self.assertEqual(new_rate, rate)
        self.assertEqual(str(new_date), date)

    def test_valid_get_rate(self):
        rate_and_date = [3.29, timezone.now()]
        self.assertEqual(_save.get_rate(rate_and_date), rate_and_date[0])

    def test_valid_get_date(self):
        rate_and_date = [3.29, timezone.now()]
        self.assertEqual(_save.get_date(rate_and_date), rate_and_date[1])

        