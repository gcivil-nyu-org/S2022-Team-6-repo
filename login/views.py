from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    context = {
        'page_name': 'CoviGuard'
    }
    return render(request, 'login/index.html', context)


def signin(request):
    return HttpResponse('signin')


def signup(request):
    return HttpResponse('signup')
