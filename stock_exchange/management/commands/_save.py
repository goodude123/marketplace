def save(currency_in_db, rate_and_date):
    if currency_in_db:
        rate = rate_and_date[0]
        date = rate_and_date[1]
        print(currency_in_db.name, 'found.')
        print('Rate, Date: ', end='')
        print(rate, date)
        currency_in_db.rate_and_date_set.create(
            rate=rate,
            date=date,
        )
        currency_in_db.save()
        print('Saved.\n')

    else:
        print('DOESN\'T FIND', currency_in_db.name)
