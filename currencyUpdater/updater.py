from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from currencyUpdater import currencyScraper


def start():
    scheduler = BackgroundScheduler()
    # used when download primary info about currency like: name, unit, code
    #scheduler.add_job(currencyScraper.get_currencies, 'interval', minutes=15)
    scheduler.add_job(currencyScraper.get_rates_and_dates, 'interval', days=1)
    scheduler.start()
