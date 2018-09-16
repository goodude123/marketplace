import os
import json
import pandas as pd
import matplotlib.pyplot as plt

class Plot:
    """ Plot object, allow to create and show diagrams, graphs. """

    def create_path(self, directory, file_name, file_extension):
        path = directory + '/' + file_name + file_extension
        return

    def save_properties_in_json_file(self):
        with open(properties_path, mode) as property_file:
            properties = property_list
            json.dump(properties, property_file)
        property_file.close()

    def __init__(self, abbr):
        self.currency_rates = None
        self.currency_info = None
        self.path = 'currencies/'
        self.abbr = abbr

    def read_data(self):
        """ Reads choosen currency data (rates, information) """
        main_directory = self.path + self.abbr
        if os.path.isdir(main_directory): # checks is currency folder exists
            json_path = main_directory + '/properties.json'
            courses_file_currency = main_directory + '/' + self.abbr + '.csv'
            if os.path.isfile(json_path): # checks is json folder exists
                with open(json_path) as json_file:
                    self.currency_info = json.load(json_file)
                json_file.close()

            if os.path.isfile(courses_file_currency): # checks is csv folder exists
                with open(courses_file_currency) as csv_file:
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
