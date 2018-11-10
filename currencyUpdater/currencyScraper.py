from ._scrap import Scrap
from stock_exchange.models import Currency
from stock_exchange.management.commands._save import save_new_rate_and_date


def get_currencies():
    scrapped = Scrap()
    scrapped.get_currencies()
    for currency in scrapped.currencies:
        if Currency.objects.filter(name=currency.name):
            print('Currency already exists in database.')
        else:
            currency_record = Currency(
                name=currency.name,
                unit=currency.unit,
                abbreviation=currency.code
            )
            currency_record.save()
            print('Saving', currency_record)


def get_rates_and_dates():
    scrapped = Scrap()
    scrapped.get_currencies()
    print('Length', len(scrapped.currencies))
    for currency in scrapped.currencies:
        currency_in_db = Currency.objects.get(name=currency.name)
        rate_and_date = [currency.rate, currency.date]

        save_new_rate_and_date(currency_in_db, rate_and_date)

    print('\nLength after adding data', len(Currency.objects.get(id=1).rate_and_date_set.all()))
