from apscheduler.schedulers.background import BackgroundScheduler
from currencyUpdater import currencyScraper


def start():
	scheduler = BackgroundScheduler
	scheduler.add_job(currencyScraper.get_currencies, 'interval', minutes=1)
	scheduler.start()
