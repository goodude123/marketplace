from django.utils import timezone
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from trading_app import errors
from stock_exchange.models import Currency


username = 'usernameindb'
password = 'zaq1@WSX'
first_name = 'john'
last_name = 'kowalski'
email = 'john@kowalski.com'


class SetUp(TestCase):
    def setUp(self):
        user = User.objects.create_user(username=username,
                                    password=password,
                                    first_name=first_name,
                                    last_name=last_name,
                                    email=email)
        user.save()

        currency = Currency.objects.create(
                                        name='dolar',
                                        unit=1,
                                        code='USD')
        currency.save()
        currency.rate_and_date_set.create(rate=1, date=timezone.now())

        self.profile = self.get_user().profile

    def get_user(self):
        user = User.objects.get(username=username)

        return user


class BuyingCurrenciesTestCase(SetUp):

    def test_model_valid_currency_bought(self):
        "Valid bought test, user has enough money to buy."
        buys_quantity = 10
        currency_primary_key = 1
        currency_code = 'USD'

        self.profile.buy(currency_primary_key, buys_quantity)
        bought = self.profile.boughtcurrency_set.get(currency_abbreviation=currency_code)

        self.assertEqual(bought.amount, 10)

    def test_model_buying_invalid_too_high_price(self):
        "Invalid bought test, user hasn't enought money."
        buys_quantity = 100000
        currency_primary_key = 1

        self.assertRaises(errors.BuyingError, lambda:
                self.profile.buy(currency_primary_key, buys_quantity))

    def test_model_buying_currencies_already_having(self):
        "Buying currencies already having. Bought currencies two times."
        buys_quantity = 5
        currency_primary_key = 1
        currency_code = 'USD'

        self.profile.buy(currency_primary_key, buys_quantity)
        self.profile.buy(currency_primary_key, buys_quantity)

        bought = self.profile.boughtcurrency_set.get(currency_abbreviation=currency_code)

        self.assertEqual(bought.amount, 2 * buys_quantity)


class SellingCurrenciesTestCase(SetUp):

    def test_model_valid_sold_currencies(self):
        "Valid sold currencies."
        buys_quantity = 10
        sells_quantity = 8
        currency_primary_key = 1
        currency_code = 'USD'

        self.profile.buy(currency_primary_key, buys_quantity)

        self.profile.sell(currency_primary_key, sells_quantity)
        already_owned_currency = self.profile.boughtcurrency_set.get(currency_abbreviation=currency_code)

        difference = buys_quantity - sells_quantity
        self.assertEqual(already_owned_currency.amount, difference)

    def test_model_invalid_sold_currencies_too_many(self):
        "Invalid test, tried to sell more currencies than had."
        buys_quantity = 2
        sells_quantity = 8
        currency_primary_key = 1

        self.profile.buy(currency_primary_key, buys_quantity)

        self.assertRaises(errors.SellingError, lambda:
                    self.profile.sell(currency_primary_key, sells_quantity))
