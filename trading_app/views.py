from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class Home(TemplateView):
    template_name = 'home.html'


@method_decorator(login_required, name='dispatch')
class User(TemplateView):
    template_name = 'user.html'
