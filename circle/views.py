from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def circle(request):
    return HttpResponse('circle')


def current_circle(request, pk):
    context = {
        'circle_id': int(pk),
        'page_name': 'Circle Info'
    }
    return render(request, 'circle/trail.html', context)


def create(create):
    return HttpResponse('create')
