from currencyUpdater._currency import Currency as SingleCurrency


def pack_currencies(currencies):
    currencies_to_template = []

    for currency in currencies:
        current_currency = create_single_currency(currency)
        currencies_to_template.append(current_currency)

    return currencies_to_template


def create_single_currency(currency):
    name = currency.name
    code = currency.code
    unit = currency.unit
    last_rate = get_last_rate(currency)
    last_date = get_last_date(currency)

    currency = SingleCurrency(
        name, unit, code, last_rate, last_date)

    return currency


def get_last_rate(currency):
    last_rate = currency.rate_and_date_set.all().latest('date').rate
    return last_rate


def get_last_date(currency):
    last_date = currency.rate_and_date_set.all().latest('date').date
    return last_date
