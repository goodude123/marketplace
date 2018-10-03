from _scrap import Scrap
from stock_exchange.models import Currency


def get_currencies():
    currencies_list = Scrap()
    currencies_list.get_currencies()
    for currency in currencies_list:
        if Currency.objects.filter(name=currency.name):
            print('Currency already exists in database.')
        else:
            currency_record = Currency(
                name=currency.name,
                unit=currency.unit,
                abbreviation=currency.abbreviation
            )
            currency_record.save()
            print('Saving', currency_record)


def get_rates_and_dates():
    currencies_list = Scrap()
    currencies_list.get_currencies()
    for currency in currencies_list:
        currency_in_db = Currency.objects.filter(name=currency.name)
        currency_in_db.rates_and_dates_set(
            rate=currency.course,
            date=currency.date
        )
        currency_in_db.save()
        print('Saving', currency_in_db.rates_and_dates)
