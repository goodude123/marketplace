from django.core.management.base import BaseCommand
from ._random_currencies import CurrenciesRandom


class Command(BaseCommand):
    help = 'Creates random courses.'

    def handle(self, *args, **options):
        random_currencies = CurrenciesRandom()

        self.stdout.write('Getting last courses.')
        random_currencies.get_currencies()
        self.stdout.write(self.style.SUCCESS('\nRandom courses saved.'))
