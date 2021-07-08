from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render


# Create your views here.

#View for Home Page.
def home(request):
    return render(request, 'face/index.html', context = None, content_type= None, status=None, using=None)

def admin_login(request):
    return render(request, 'face/login.html')


def dashboard(request):
    return render(request, 'face/dashboard.html')

def login(request, name, password):
    name=''
    password = ""
    return render(request,)
