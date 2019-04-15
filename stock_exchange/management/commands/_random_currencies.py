import random
import warnings
from datetime import datetime
from stock_exchange.models import Currency
from ._save import save_new_rate_and_date


class CurrenciesRandom:

    def get_currencies(self):
        warnings.filterwarnings("ignore", category=RuntimeWarning)

        for currency in Currency.objects.all():

            last_rate = currency.rate_and_date_set.order_by('-date')[0].rate
            currency_in_db = Currency.objects.get(name=currency.name)

            # here go logic of random modifying rates
            new_random_rate = self.modify_rate(last_rate)
            current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            rate_and_date = [new_random_rate, current_date]

            save_new_rate_and_date(currency_in_db, rate_and_date)

    def modify_rate(self, rate):
        operation = self.choose_operation()
        if operation == 'subtraction':
            if self.subtract(rate) <= 0:
                return self.add(rate)
            else:
                return self.subtract(rate)
        elif operation == 'addition':
            return self.add(rate)

    def choose_operation(self):
        operations = ['addition', 'subtraction']

        return operations[random.randrange(2)]

    def add(self, rate):
        result = round(rate + random.uniform(0.001, 0.002), 4)

        return result

    def subtract(self, rate):
        result = round(rate - random.uniform(0.001, 0.002), 4)

        return result
