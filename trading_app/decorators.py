from django.urls import reverse
from django.shortcuts import redirect


def prevent_logged_users(function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('trading_app:home'))
        else:
            return function(request, *args, **kwargs)
    wrapper.__doc__ = function.__doc__
    wrapper.__name__ = function.__name__

    return wrapper


def prevent_logged_users_class_decorator(function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('trading_app:home'))
        else:
            return function(request, *args, **kwargs)
    return wrapper
