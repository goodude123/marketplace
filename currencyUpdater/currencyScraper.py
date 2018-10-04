from ._scrap import Scrap
from stock_exchange.models import Currency
#import warnings


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
        # warnings.filterwarnings("ignore", category=RuntimeWarning) 
        currency_in_db = Currency.objects.get(name=currency.name)
        if currency_in_db:
            print('CURRENCY_IN_DB:', currency_in_db)
            print('rate, Date: ', end=' ')
            print(currency.rate, currency.date)
            currency_in_db.rate_and_date_set.create(
                rate=currency.rate,
                date=currency.date
            )
            currency_in_db.save()
            print('Saving', currency_in_db.rate_and_date_set.all())
            print()
        else:
            print('DOESNT FIND', currency.name)

    print('\nLength after adding data', len(Currency.objects.get(id=1).rate_and_date_set.all()))
