from django.apps import AppConfig


class StockExchangeConfig(AppConfig):
    name = 'stock_exchange'

    def ready(self):
        from currencyUpdater import updater
        updater.start()
