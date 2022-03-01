from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    context = {
        'page_name': 'CoviGuard',
        'css_name': 'login'
    }
    return render(request, 'login/index.html', context)


def signin(request):
    context = {
        'page_name': 'SignIn'
    }
    return render(request, 'login/signin.html', context)


def signup(request):
    context = {
        'page_name': 'SignUp'
    }
    return render(request, 'login/signup.html', context)
