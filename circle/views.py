from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def circle(request):
    context = {
        'page_name': 'Circle'
    }
    return render(request, 'circle/circle.html', context)


def current_circle(request, pk):
    context = {
        'circle_id': int(pk),
        'page_name': 'Circle Info'
    }
    return render(request, 'circle/current-circle.html', context)


def create(request):
    context = {
        'page_name': 'Create'
    }
    return render(request, 'circle/add.html', context)
