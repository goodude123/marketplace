import matplotlib.pyplot as plt
from currencylocals import LocalCurrency


class Plot(LocalCurrency):
    """ Plot object, allow to create and show diagrams, graphs. """
    def __init__(self, abbr):
        super().__init__(abbr)
        self.currency_rates = None
        self.currency_info = None

    def create_graph(self):
        """ Creates and show graph from data """
        self.read_data()
        date_list = self.currency_rates['Date'].tolist()
        rates_list = self.currency_rates['Rate'].tolist()

        print(date_list, rates_list)
