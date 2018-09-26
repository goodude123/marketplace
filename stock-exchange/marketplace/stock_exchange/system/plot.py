import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from currency_files import LocalCurrency


class PlotCurrency(LocalCurrency):
    def __init__(self, abbr):
        super().__init__(abbr)
        self.assign_values()

    def assign_values(self):
        if self.is_main_directory():
            self.currency_rates = self.get_rates_from_csv_as_dataframe()
            self.full_name = self.get_properties_from_json()[0]
            self.unit = self.get_properties_from_json()[1]
            self.abbreviation = self.get_properties_from_json()[2]

    def convert_date_to_pandas_datetime(self):
        self.currency_rates['Date'] = pd.to_datetime(
            self.currency_rates['Date'])

    def convert_date_to_pandas_datetime_without_time(self):
        self.currency_rates['Date'] = self.currency_rates['Date'].dt.normalize()

    def get_dates(self):
        return self.currency_rates['Date']

    def get_rates(self):
        return self.currency_rates['Rate']

    def show_values(self):
        print(self.currency_rates)
        print(self.full_name)
        print(self.unit)
        print(self.abbreviation)


class Plot:
    """ Plot object, allow to create and show diagrams, graphs. """
    def __init__(self, abbr):
        self.abbr = abbr
        self.plot = None

    def create_graph(self):
        """ Creates and show graph from data """
        currency_data = PlotCurrency(self.abbr)
        currency_data.convert_date_to_pandas_datetime()
        currency_data.show_values()

        x = currency_data.get_dates()[-10:]
        y = currency_data.get_rates()[-10:]

        fig, ax = plt.subplots()

        fig.suptitle(currency_data.full_name)

        ax.plot(x, y)

        formatter = ticker.FormatStrFormatter('%1.2f')
        ax.yaxis.set_major_formatter(formatter)

        for tick in ax.yaxis.get_major_ticks():
            tick.label1On = False
            tick.label2On = True
            tick.label2.set_color('green')

        plt.show()
