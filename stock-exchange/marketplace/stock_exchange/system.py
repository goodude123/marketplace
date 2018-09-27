from currency import Currencies
from .. import models


class CurrencyDjangoDataRecord(Currencies):
    def save_currenies_info_in_db(self):
        models.Currency.objects.all()
        models.Rate_and_date.all()


a = CurrencyDjangoDataRecord()
a.save_currenies_info_in_db()
