from _scrap import Scrap
from stock_exchange.models import Rate_and_date, Currency


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
                abbreviation=currency.abbreviation)
            currency_record.save()
