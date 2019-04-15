from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, FormView, ListView
from django.utils.decorators import method_decorator
from django.contrib.auth import login, authenticate
from django.urls import reverse
from django.shortcuts import render, redirect
from trading_app.forms import SignUpForm, BuyCurrencyForm, SellCurrencyForm
from trading_app.decorators import prevent_logged_users, prevent_logged_users_class_decorator
from stock_exchange.models import Currency


class Home(TemplateView):
    template_name = 'home.html'


@method_decorator(login_required, name='dispatch')
class User(TemplateView):
    template_name = 'user.html'


@method_decorator(prevent_logged_users_class_decorator, name='dispatch')
class SignUpView(FormView):
    form_class = SignUpForm
    template_name = 'sign_up.html'

    def form_valid(self, form):
        form.save()  # user is already saved
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        authenticated_user = authenticate(username=username, password=password)
        login(request, authenticated_user)
        return redirect(reverse('trading_app:home'))



@method_decorator(login_required, name='dispatch')
class OwnedCurrenciesView(TemplateView):
    template_name = 'owned_currencies.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owned'] = self.request.user.profile.boughtcurrency_set.all()
        return context


class BuyCurrencyView(FormView):
    form_class = BuyCurrencyForm
    template_name = 'buy_currencies.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial_code'] = self.kwargs['initial']
        return kwargs

    def form_valid(self, form):
        currency_code = form.cleaned_data.get('currency_code')
        quantity = form.cleaned_data.get('quantity')
        self.request.user.profile.buy(currency_code, quantity)

        return redirect(reverse('trading_app:owned_currencies'))
    
    def form_invalid(self, form):
        return render(self.request, 'buy_currencies.html', {'form': form, 'initial': initial})        


class SellCurrencyView(FormView):
    form_class = SellCurrencyForm
    template_name = 'sell_currencies.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial_code'] = self.kwargs['initial']
        kwargs['user'] = self.request.user

        if self.request.method in ('POST'):
            kwargs.update({
                'data': self.request.POST,
                'user': self.request.user,
            })
        return kwargs

    def form_valid(self, form):
        currency_index  = int(form.cleaned_data.get('currencies'))
        # convert back from api index to database index
        number_of_objects = len(Currency.objects.all())
        last_id = Currency.objects.order_by('-pk')[0].pk
        difference = last_id - number_of_objects + 1
        currency_index += difference

        quantity = form.cleaned_data.get('quantity')
        self.request.user.profile.sell(currency_index, quantity)

        return redirect(reverse('trading_app:owned_currencies'))
    
    def form_invalid(self, form):
        return render(self.request, 'sell_currencies.html', {'form': form})
