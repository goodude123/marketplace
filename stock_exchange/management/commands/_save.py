def save_new_rate_and_date(currency_in_db, rate_and_date):
    if currency_in_db:
        rate = get_rate(rate_and_date)
        date = get_date(rate_and_date)
        print_info(currency_in_db, rate_and_date)
        currency_in_db.rate_and_date_set.create(
            rate=rate,
            date=date,
        )
        currency_in_db.save()


def get_rate(rate_and_date):
    rate = rate_and_date[0]
    return rate

def get_date(rate_and_date):
    date = rate_and_date[1]
    return date

def print_info(currency, rate_and_date):
    print(currency.name, 'found.')
    print('Rate, Date: ', end='')
    rate = get_rate(rate_and_date)
    date = get_date(rate_and_date)
    print(rate, date)
