from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from .forms import SignUpForm
from .models import UserData
from circle.models import CircleUser
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

class SignUp(CreateView):
    #Added feild and modified UserCreationForm for min login/forms.py
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "login/signup.html"

def login(request):
    email_id=request.POST.get('email')
    user=UserData.objects.get(email=email_id)
    circle_user_data = CircleUser.objects.filter(username=user.username)
    context = {
        'page_name': 'Circle',
        'circle_user_data': circle_user_data,
        'username': user.username
    }
    return render(request, 'circle/circle.html', context)



def createuser(request):
        if request.method == 'POST':
            if request.POST.get('email') and request.POST.get('password'):
                userdata=UserData()
                userdata.firstname= request.POST.get('firstname')
                userdata.lastname= request.POST.get('lastname')
                userdata.username= request.POST.get('username')
                userdata.password= request.POST.get('password')
                userdata.email= request.POST.get('email')
                userdata.dob= request.POST.get('DoB')
                userdata.phone= request.POST.get('phonenumber')
                userdata.work_address= request.POST.get('ZipWork')
                userdata.home_adress= request.POST.get('ZipHome')
                is_vaxxed=False
                if request.POST.get('vaccination') == 1:
                    is_vaxxed=True
                userdata.is_vacinated= is_vaxxed
                userdata.save()
                return render(request, 'login/index.html')

        else:
                return render(request,'login/signup.html')

