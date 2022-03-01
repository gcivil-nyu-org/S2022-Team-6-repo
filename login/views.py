from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    return HttpResponse('index')


def signin(request):
    return HttpResponse('signin')


def signup(request):
    return HttpResponse('signup')
