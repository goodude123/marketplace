from stock_exchange.models import Currency
from ._currency import SingleCurrency
from ._request_handle import simple_get
from bs4 import BeautifulSoup
from datetime import datetime


class Scrap:

    def __init__(self):
        self.url = 'https://www.nbp.pl/home.aspx?f=/kursy/kursya.html'
        self.currencies = []

    def create_html_code(self):
        """ Creates bs4 html code model """

        raw_html = simple_get(self.url)
        bs4_html = BeautifulSoup(raw_html, 'html.parser')

        return bs4_html

    def get_currency_properties(self, table_cells):
        """ Gets values from table_cells """
        name = table_cells[0].contents[0]
        unit, abbreviation = table_cells[1].contents[0].split()
        rate = float(table_cells[2].contents[0].replace(',', '.'))
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        return [name, unit, abbreviation, rate, date]

    def scrap_currencies(self):
        """ Finds data in bs4 html, get contents and creates Currency models"""

        html = self.create_html_code()
        for table in html.findAll('table'):

            # find correct table
            if table.parent.get('id') == 'article':

                # iterate through table rows
                for table_row in table.findAll('tr')[3:38]:
                    table_data_cells = table_row.findAll('td')
                    currency_properties = SingleCurrency(
                        *self.get_currency_properties(table_data_cells)
                    )

                    self.currencies.append(currency_properties)

    def save_currency_information(self):
        self.scrap_currencies()
        for currency in self.currencies:
            if Currency.objects.filter(name=currency.name):
                print('Currency already exists in database.')
            else:
                currency_record = SingleCurrency(
                    name=currency.name,
                    unit=currency.unit,
                    abbreviation=currency.code
                )
                currency_record.save()
                print('Saving', currency_record)

    def save_rates_and_dates(self):
        self.scrap_currencies()
        print(self.currencies)
        print('Length', len(self.currencies))
        for currency in self.currencies:
            # warnings.filterwarnings("ignore", category=RuntimeWarning)
            currency_in_db = Currency.objects.get(name=currency.name)
            if currency_in_db:
                print('CURRENCY_IN_DB:', currency_in_db)
                print('Rate, Date: ', end=' ')
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
