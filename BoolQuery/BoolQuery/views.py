from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse("Welcome to Bool Query Search Engine!")


def hello(request):
    context = {}
    context['hello'] = 'Welcome to Bool Query Search Engine!'
    return render(request, 'index.html', context)
