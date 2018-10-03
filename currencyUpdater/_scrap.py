from _currency import Currency
from _request_handle import simple_get
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

    def get_currencies(self):
        """ Finds data in bs4 html, get contents and creates Currency models"""

        html = self.create_html_code()
        for table in html.findAll('table'):

            # find correct table
            if table.parent.get('id') == 'article':

                # iterate through table rows
                for table_row in table.findAll('tr')[3:38]:
                    table_data_cells = table_row.findAll('td')
                    currency_properties = Currency(
                        *self.get_currency_properties(table_data_cells)
                    )

                    self.currencies.append(currency_properties)
