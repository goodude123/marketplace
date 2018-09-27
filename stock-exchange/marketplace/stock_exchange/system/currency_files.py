import os
import json
import random
import pandas as pd
from datetime import datetime
from currency import Currency
from request_handle import simple_get
from bs4 import BeautifulSoup


class LocalCurrency:
    def __init__(self, abbr):
        self.path = 'currencies/'
        self.abbr = abbr
        self.currency_directory_path = self.path + self.abbr + '/'

    def get_properties_from_json(self):
        """ Gets values from json file """
        properties_json_file = self.currency_directory_path + 'properties.json'
        if os.path.isfile(properties_json_file):
            with open(properties_json_file) as json_file:
                currency_info = json.load(json_file)
            json_file.close()
            return currency_info

    def get_rates_from_csv_as_dataframe(self):
        """ Gets courses from csv file and return it as DataFram """
        rates_csv_file = self.currency_directory_path + self.abbr + '.csv'
        if os.path.isfile(rates_csv_file):
            with open(rates_csv_file) as csv_file:
                currency_rates_as_dataframe = pd.read_csv(csv_file)
            csv_file.close()
            return currency_rates_as_dataframe

    def is_main_directory(self):
        """ Check is main directory exists """
        main_directory = self.path + self.abbr
        return os.path.isdir(main_directory)


class CurrenciesFile:
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

    def set_path_to_save_all_files(self):
        return 'currencies/'

    def create_path(self, directory, file_name, file_extension):
        path = directory + '/' + file_name + file_extension
        return path

    def set_write_mode(self):
        return 'w'

    def set_append_mode(self):
        return 'a'

    def set_columns_names(self):
        return ['Rate', 'Date']

    def get_course_and_date(self, currency):
        return [currency.course, currency.date]

    def check_mode_and_set_header(self, mode):
        if mode == 'a':
            header = False
        else:
            header = True
        return header

    def create_new_or_append_to_file_courses(self, file, mode, courses):
        courses_in_data_frame = pd.DataFrame(
            [courses], columns=self.set_columns_names())

        with open(file, mode) as file:
            courses_in_data_frame.to_csv(
                file, header=self.check_mode_and_set_header(mode), index=False
            )
        file.close()

    def save_properties_in_json_file(self):
        with open(properties_path, mode) as property_file:
            properties = property_list
            json.dump(properties, property_file)
        property_file.close()

    def save_currencies(self):
        """ Save currency information as (course, course date, abbreviation)"""
        main_directory_path = self.set_path_to_save_all_files()
        for currency in self.currencies:
            directory_currency = main_directory_path + currency.code

            courses_file_currency = self.create_path(
                directory_currency, currency.code, '.csv')

            properties_currency_file = self.create_path(
                directory_currency, 'properties', '.json')

            # if directory for each currency doesnt exists make it
            if not os.path.exists(directory_currency):
                os.makedirs(directory_currency)

            # if info file doesnt exists make it (save in json currency obj)
            if not os.path.exists(properties_currency_file):
                with open(properties_currency_file, 'w') as file:
                    info = [currency.name, currency.unit, currency.code]
                    json.dump(info, file)
                file.close()

            course_and_date = self.get_course_and_date(currency)

            if not os.path.exists(courses_file_currency):
                # create new file
                self.create_new_or_append_to_file_courses(
                    courses_file_currency,
                    self.set_write_mode(),
                    course_and_date
                )
            else:
                # append to file
                self.create_new_or_append_to_file_courses(
                    courses_file_currency,
                    self.set_append_mode(),
                    course_and_date
                )


class CurrenciesRandomCoursesFile(CurrenciesFile):
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
                if self.subtract(currency) <= 0:
                    currency.course = self.add(currency)
                else:
                    currency.course = self.subtract(currency)
            elif operation == 'addition':
                currency.course = self.add(currency)
