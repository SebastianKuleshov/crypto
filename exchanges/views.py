from django.shortcuts import render

from .utils import get_token_prices
# Create your views here.

def index(request):
    data = get_token_prices()

    return render(request, 'index.html', context={'data': data})
