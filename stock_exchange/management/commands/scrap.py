from django.core.management.base import BaseCommand
from ._scrap import Scrap


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument(
            '--new',
            action='store_true',
            dest='new',
            help='Saves currency info records.',
        )

        parser.add_argument(
            '--update',
            action='store_true',
            dest='update',
            help='Saves currency courses.'
        )

    def handle(self, *args, **options):
        scrapper = Scrap()

        if options['new']:
            self.stdout.write('Scraping currency informations.')
            scrapper.save_currency_information()
            self.stdout.write(self.style.SUCCESS('Saved informations.'))

        if options['update']:
            self.stdout.write('Scraping currency courses.')
            scrapper.save_rates_and_dates()
            self.stdout.write(self.style.SUCCESS('Saved courses.'))
