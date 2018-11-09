from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from stock_exchange.models import Currency
from trading_app import errors


class Profile(models.Model):
    "Extended user profile."
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    money = models.FloatField(default=100)

    def __str__(self):
        return self.user.username

    def buy(self, to_bought_index, quantity):
        "Substracs price from money and adds currencies to owned."

        rate = self.__get_currency_last_rate(to_bought_index)
        unit = self.__get_currency_unit(to_bought_index)
        price = round(rate * quantity * unit, 5)

        code = self.__get_currency_code(to_bought_index)

        if price <= self.money:
            self.money -= price
            self.save()
            try:
                already_bought = self.boughtcurrency_set.filter(currency_abbreviation=code)[0]
            except IndexError:
                already_bought = False

            if already_bought:
                already_bought.amount += quantity
                already_bought.save()
            else:
                buys = self.boughtcurrency_set.create(
                                        currency_abbreviation=code.upper(),
                                        amount=quantity)
                buys.save()
        else:
            raise errors.BuyingError('Too high price!')

    def sell(self, index_to_database, quantity):
        "Deletes currencies from profile owned, adds money."

        rate = self.__get_currency_last_rate(index_to_database) - 0.004
        code = self.__get_currency_code(index_to_database)
        unit = self.__get_currency_unit(index_to_database)

        try:
            owned_selling_currency = self.boughtcurrency_set.get(currency_abbreviation=code)
            if owned_selling_currency.amount >= quantity:
                owned_selling_currency.amount -= quantity
                owned_selling_currency.save()
                if owned_selling_currency.amount == 0:
                    owned_selling_currency.delete()
                self.money += round(rate * quantity * unit, 5)
                self.save()
            else:
                raise errors.SellingError('You dont have enough currencies')
        except ObjectDoesNotExist:
            print('You never had that currency.')

    def __get_owned_currencies(self):
        owned = self.boughtcurrency_set.all()
        return owned

    def __get_currency_from_database(self, currency_index):
        currency = Currency.objects.get(pk=currency_index)
        return currency

    def __get_currency_unit(self, currency_index):
        currency = Currency.objects.get(pk=currency_index)
        return currency.unit

    def __get_currency_code(self, currency_index):
        currency = self.__get_currency_from_database(currency_index)
        return currency.code

    def __get_currency_last_rate(self, currency_index):
        bought_currency = self.__get_currency_from_database(currency_index)
        rate = bought_currency.rate_and_date_set.all().order_by('-date')[0].rate

        return rate


class BoughtCurrency(models.Model):
    "Currency already bought by user."

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    currency_abbreviation = models.CharField(max_length=8)
    amount = models.IntegerField()

    def __str__(self):
        designation = self.currency_abbreviation + ' ' + self.profile.user.username + ' owned.'
        return designation


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
