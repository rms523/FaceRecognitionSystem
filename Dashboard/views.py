import os
import time
import mysql.connector
from django.conf import settings
# from django.template import loader
from django.shortcuts import render, reverse
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout


def log(str_message):
    log_filename = os.path.join(settings.PROJECT_PATH, 'logs', 'log.txt')
    file_handle = open(log_filename, 'a')
    now = time.localtime()
    f = '%Y-%m-%d %H:%M:%S'
    print(str_message)
    file_handle.write(time.strftime(f, now) + '\t' + str_message + '\n')
    file_handle.close()


try:
    connection = mysql.connector.connect(host='localhost', database='facerecognition', user='root', password='')
except mysql.connector.Error as e:
    print(e)


def home(request):
    return render(request, 'Dashboard/index.html', context=None, content_type=None, status=None, using=None)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        log(username)
        log(password)

        if not connection.is_connected():
            return render(request, 'Dashboard/login.html', {
                'error_message': 'Error in login'
            })

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('Dashboard:dashboard'))
            else:
                return render(request, 'Dashboard/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'Dashboard/login.html', {'error_message': 'Invalid login credentials.'})

    return render(request, 'Dashboard/login.html')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('Dashboard:login_user'))


def dashboard(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('Dashboard:login_user'))

    return render(request, 'Dashboard/dashboard.html')


def add_person(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('Dashboard:login_user'))

    if request.method == "POST":
        fullname = request.POST['fullname']
        age = request.POST['age']
        imagefile = request.POST['imagefile']
        log(imagefile)

    return render(request, "Dashboard/add_person.html")


def search_person(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('Dashboard:login_user'))



    return render(request, "Dashboard/search.html")


def view_info(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    return render(request, "Dashboard/view.html")


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2:
            return render(request, 'Dashboard/register.html', {'error_message': 'Your Passwords did not match.'})
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        # contact = request.POST['contact']
        contact = ' '
        # home_address = request.POST['home_address']
        home_address = ' '

        if connection.is_connected():
            cursor = connection.cursor()
            query = "insert into guardian_info " + \
                    "(firstname, lastname, email, password, contact, address) " + \
                    "VALUES('%s','%s','%s','%s','%s','%s')" % (firstname, lastname, username, password1,
                                                               contact, home_address)
            # query = """INSERT INTO guardian_info (firstname, lastname, email, password, contact, address) VALUES('%s','%s','%s','%s','%s','%s')""" % (
            #firstname, lastname, username, password1, contact, home_address)
            log(query)
            cursor.execute(query)

            connection.commit()

            user = User.objects.create_user(username=username, password=password1)
            user.save()

        else:
            return render(request, 'Dashboard/register.html', {'error_message': 'Issue in DB connection.'})
        return HttpResponseRedirect(reverse('Dashboard:login_user'))
    return render(request, "Dashboard/register.html")
