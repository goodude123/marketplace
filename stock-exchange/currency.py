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

    def __init__(self, name, value, code, course, date):
        self.name = name
        self.value = value
        self.code = code
        self.course = course
        self.date = date


class Data:
    """ All scrapped data class """

    def __init__(self):
        """ Create empty data object """

        self.url = 'https://www.nbp.pl/home.aspx?f=/kursy/kursya.html'
        self.currencies = []


    def get_bs4(self):
        """ Creates bs4 html code model """

        raw_html = simple_get(self.url)
        bs4_html = BeautifulSoup(raw_html, 'html.parser')

        return bs4_html


    def get_currencies(self):
        """ Finds data in bs4 html, get contents and creates Currency models"""

        html = self.get_bs4()
        for table in html.findAll('table'):

            # find correct table
            if table.parent.get('id') == 'article':

                # iterate through table rows
                for tr in table.findAll('tr')[3:38]:
                    tds = tr.findAll('td')[:3]
                    args = []

                    # unpack content from table data
                    args.append(tds[0].contents[0]) # currency name
                    args.extend(tds[1].contents[0].split()) # unit and abbr
                    args.append(float(tds[2].contents[0].replace(',', '.'))) # rate
                    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # date
                    args.append(date)

                    self.currencies.append(Currency(*args))

    def save_currencies(self):
        """ Save currency information as (course, course date, abbreviation) """
        path = 'currencies/'
        for currency in self.currencies:
            directory = path + currency.code
            # if directory for each currency doesnt exists make it
            if not os.path.exists(directory):
                os.makedirs(directory)

            info_path = directory + '/information.json'
            # if info file doesnt exists make it (save in json currency obj)
            if not os.path.exists(info_path):
                with open(info_path, 'w') as file:
                    info = [currency.name, currency.value, currency.code]
                    json.dump(info, file)
                file.close()

            # path to csv file for each currency
            csv_path = directory + '/' + currency.code + '.csv'
            data = [[currency.course, currency.date]]

            if not os.path.exists(csv_path):
                # create new file
                with open(csv_path, 'w') as file:
                    df = pd.DataFrame(data, columns=['Rate', 'Date'])
                    df.to_csv(file, index=False)
                file.close()
            else:
                # append to file
                df = pd.DataFrame(data, columns=['Rate', 'Date'])
                with open(csv_path, 'a') as file:
                    df.to_csv(file, header=False, index=False)
                file.close()


class RandomData(Data):
    """ Creates random currency rates from scrapped data """
    def __init__(self):
        super().__init__()
        self.get_currencies()

    def choose_operation(self):
        operations = ['addition', 'subtraction']

        return operations[random.randrange(2)]

    def addition(self, object):
        result = round(object.course + random.uniform(0.1, 0.2), 4)

        return result

    def subtracion(self, object):
        result = round(object.course - random.uniform(0.1, 0.2), 4)

        return result

    def edit_currency(self):
        for currency in self.currencies:
            operation = self.choose_operation()
            if operation == 'subtraction':
                if self.subtracion(currency) <= 0 :
                    currency.course = self.addition(currency)
                else:
                    currency.course = self.subtracion(currency)
            elif operation == 'addition':
                currency.course = self.addition(currency)


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
            json_path = directory + '/information.json'
            csv_path = directory + '/' + self.abbr + '.csv'
            if os.path.isfile(json_path): # checks is json folder exists
                with open(json_path) as json_file:
                    self.currency_info = json.load(json_file)
                json_file.close()

            if os.path.isfile(csv_path): # checks is csv folder exists
                with open(csv_path) as csv_file:
                    df = pd.read_csv(csv_file)
                    self.currency_rates = df
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

    scrapped = Data()
    scrapped.get_currencies()
    scrapped.save_currencies()
    print(scrapped.currencies)

    rand = RandomData()
    rand.edit_currency()
    rand.save_currencies()
    print(rand.currencies)

    plot = Plot('USD')
    plot.create_graph()
