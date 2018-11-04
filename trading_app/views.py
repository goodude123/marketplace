from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth import login, authenticate
from django.urls import reverse
from django.shortcuts import render, redirect
from trading_app.forms import SignUpForm, BuyCurrencyForm, SellCurrencyForm
from trading_app.decorators import prevent_logged_users


class Home(TemplateView):
    template_name = 'home.html'


@method_decorator(login_required, name='dispatch')
class User(TemplateView):
    template_name = 'user.html'


@prevent_logged_users
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()  # user is already saved
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            authenticated_user = authenticate(username=username, password=password)
            login(request, authenticated_user)
            return redirect(reverse('trading_app:home'))
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def owned_currencies(request):
    owned = request.user.profile.boughtcurrency_set.all()
    return render(request, 'owned_currencies.html', {'owned': owned})


@login_required
def buy_currencies(request, initial):
    if request.method == 'POST':
        form = BuyCurrencyForm(data=request.POST)
        if form.is_valid():
            currency_code = form.cleaned_data.get('currency_code')
            quantity = form.cleaned_data.get('quantity')
            request.user.profile.buy(currency_code, quantity)

            return redirect(reverse('trading_app:owned_currencies'))

        return render(request, 'buy_currencies.html', {'form': form, 'initial': initial})

    else:
        form = BuyCurrencyForm(initial_code=initial)
        return render(request, 'buy_currencies.html', {'form': form, 'initial': initial})


@login_required
def sell_currencies(request, initial):
    if request.method == 'POST':
        form = SellCurrencyForm(data=request.POST, user=request.user)
        if form.is_valid():
            currency_code = form.cleaned_data.get('currency_code')
            quantity = form.cleaned_data.get('quantity')
            request.user.profile.sell(currency_code, quantity)

            return redirect(reverse('trading_app:owned_currencies'))
        
        return render(request, 'sell_currencies.html', {'form': form})
    else:
        data = {'initial_code': initial, 'user': request.user}
        form = SellCurrencyForm(**data)
        return render(request, 'sell_currencies.html', {'form': form})
