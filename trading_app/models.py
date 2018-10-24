from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from stock_exchange.models import Currency
from trading_app import errors


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    money = models.IntegerField(default=100)

    def __str__(self):
        return self.user.username

    def buy(self, to_bought, quantity):
        rate = self.get_last_rate(to_bought)
        price = rate * quantity

        if price <= self.money:
            self.money -= price
            try: 
                already_bought = self.boughtcurrency_set.filter(currency_abbreviation=to_bought.upper())[0]
            except IndexError:
                already_bought = False

            if already_bought:
                already_bought.amount += quantity
                already_bought.save()
            else:
                buys = self.boughtcurrency_set.create(
                                        currency_abbreviation=to_bought.upper(),
                                        amount=quantity
                                        )
                buys.save()
        else:
            raise errors.BuyingError('Too high price!')

    def sell(self, to_sell, quantity):
        rate = self.get_last_rate(to_sell) - 0.004

        try:
            owned_currency = self.boughtcurrency_set.get(currency_abbreviation=to_sell.upper())
            if owned_currency.amount >= quantity:
                owned_currency.amount -= quantity
                owned_currency.save()
                self.money += rate * quantity
            else:
                raise errors.SellingError('You dont have enough currencies')
        except ObjectDoesNotExist:
            print('You never had that currency.')

    def get_last_rate(self, currency_code):
        currency_bought = Currency.objects.get(code=currency_code.upper())
        rate = currency_bought.rate_and_date_set.all().order_by('-date')[0].rate

        return rate


class BoughtCurrency(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    currency_abbreviation = models.CharField(max_length=8)
    amount = models.IntegerField()

    def __str__(self):
        designation = self.profile.user.username + ' owned.'
        return designation


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
