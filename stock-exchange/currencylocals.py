import os
import json
import pandas as pd


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
