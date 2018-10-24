from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User as django_user
from django.urls import reverse
from django.shortcuts import render, redirect
from trading_app.forms import SignUpForm
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
            print(form.cleaned_data.get('username'))
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            authenticated_user = authenticate(username=username, password=password)
            login(request, authenticated_user)
            return redirect(reverse('trading_app:home'))
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
