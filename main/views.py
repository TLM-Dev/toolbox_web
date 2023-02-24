from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseBadRequest

# Create your views here.

class MainView(TemplateView):
    template_name = 'main.html'
    success_url = '/'