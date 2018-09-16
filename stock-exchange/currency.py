import os
import json
import random
import pandas as pd
import matplotlib.pyplot as plt
from request_handle import simple_get
from bs4 import BeautifulSoup
from datetime import datetime


class Currency:
    """ Simple currency class """

    def __init__(self, name, unit, code, course, date):
        self.name = name
        self.unit = unit
        self.code = code
        self.course = course
        self.date = date


class Currencies:
    """ All scrapped data class """

    def __init__(self):
        """ Create empty data object """

        self.url = 'https://www.nbp.pl/home.aspx?f=/kursy/kursya.html'
        self.currencies = []


    def create_html_code(self):
        """ Creates bs4 html code model """

        raw_html = simple_get(self.url)
        bs4_html = BeautifulSoup(raw_html, 'html.parser')

        return bs4_html

    def get_currency_properties(self, table_cells):
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
                    """
                    currency_properties = []
                    currency_properties.extend(self.get_currency_properties(table_data_cells))
                    """
                    currency_properties = Currency(*self.get_currency_properties(table_data_cells))

                    self.currencies.append(currency_properties)

    def save_currencies(self):
        """ Save currency information as (course, course date, abbreviation) """
        path = 'currencies/'
        for currency in self.currencies:
            directory = path + currency.code
            # if directory for each currency doesnt exists make it
            if not os.path.exists(directory):
                os.makedirs(directory)

            info_path = directory + '/properties.json'
            # if info file doesnt exists make it (save in json currency obj)
            if not os.path.exists(info_path):
                with open(info_path, 'w') as file:
                    info = [currency.name, currency.unit, currency.code]
                    json.dump(info, file)
                file.close()

            # path to csv file for each currency
            csv_path = directory + '/' + currency.code + '.csv'
            data = [[currency.course, currency.date]]

            if not os.path.exists(csv_path):
                # create new file
                with open(csv_path, 'w') as file:
                    data_read_from_file = pd.DataFrame(data, columns=['Rate', 'Date'])
                    data_read_from_file.to_csv(file, index=False)
                file.close()
            else:
                # append to file
                data_read_from_file = pd.DataFrame(data, columns=['Rate', 'Date'])
                with open(csv_path, 'a') as file:
                    data_read_from_file.to_csv(file, header=False, index=False)
                file.close()


class CurrenciesRandomCourses(Currencies):
    """ Creates random currency rates from scrapped data """
    def __init__(self):
        super().__init__()
        self.get_currencies()

    def choose_operation(self):
        operations = ['addition', 'subtraction']

        return operations[random.randrange(2)]

    def add(self, object):
        result = round(object.course + random.uniform(0.1, 0.2), 4)

        return result

    def subtract(self, object):
        result = round(object.course - random.uniform(0.1, 0.2), 4)

        return result

    def random_edit_course_value(self):
        for currency in self.currencies:
            operation = self.choose_operation()
            if operation == 'subtraction':
                if self.subtract(currency) <= 0 :
                    currency.course = self.add(currency)
                else:
                    currency.course = self.subtract(currency)
            elif operation == 'addition':
                currency.course = self.add(currency)


class Plot:
    """ Plot object, allow to create and show diagrams, graphs. """
    def __init__(self, abbr):
        self.currency_rates = None
        self.currency_info = None
        self.path = 'currencies/'
        self.abbr = abbr

    def read_data(self):
        """ Reads choosen currency data (rates, information) """
        directory = self.path + self.abbr
        if os.path.isdir(directory): # checks is currency folder exists
            json_path = directory + '/properties.json'
            csv_path = directory + '/' + self.abbr + '.csv'
            if os.path.isfile(json_path): # checks is json folder exists
                with open(json_path) as json_file:
                    self.currency_info = json.load(json_file)
                json_file.close()

            if os.path.isfile(csv_path): # checks is csv folder exists
                with open(csv_path) as csv_file:
                    data_read_from_file = pd.read_csv(csv_file)
                    self.currency_rates = data_read_from_file
                csv_file.close()

    def create_graph(self):
        """ Creates and show graph from data """
        self.read_data()
        #self.currency_rates.plot(x='Date', y='Rate')
        date_list = self.currency_rates['Date'].tolist()
        rates_list = self.currency_rates['Rate'].tolist()

        print(date_list, rates_list)
"""
        f, ax = plt.subplots(1)
        ax.plot(date_list, rates_list)
        ax.set_ylim(ymin=0)
        plt.show(f)
"""

if __name__ == '__main__':
    # scrap data and save it in files

    scrapped = Currencies()
    scrapped.get_currencies()
    scrapped.save_currencies()
    print(scrapped.currencies)

    rand = RandomData()
    rand.random_edit_course_value()
    rand.save_currencies()
    print(rand.currencies)

    plot = Plot('USD')
    plot.create_graph()
