from currencyUpdater._currency import Currency as SingleCurrency


def pack_currencies(currencies):
    currencies_to_template = []

    for currency in currencies:
        name = currency.name
        code = currency.code
        unit = currency.unit
        last_rate = currency.rate_and_date_set.all().latest('date').rate
        last_date = currency.rate_and_date_set.all().latest('date').date

        currenct_currency = SingleCurrency(
            name, unit, code, last_rate, last_date)

        # currencies in list ()
        currencies_to_template.append(currenct_currency)

    return currencies_to_template
