from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

#testing
# Create your views here.

#View for Home Page.
def home(request):
    return render(request, 'Dashboard/index.html', context = None, content_type= None, status=None, using=None)

def admin_login(request):
    return render(request, 'Dashboard/login.html')


def dashboard(request):
    return render(request, 'Dashboard/dashboard.html')

def login(request, name, password):
    name=''
    password = ""
    return render(request,)
