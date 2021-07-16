import os
import time
import mysql.connector
from django.conf import settings
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
    connection = mysql.connector.connect(host='localhost', database='missingly_db', user='root', password='')
except mysql.connector.Error as e:
    print(e)

def update_person_missing_status(request, search_id):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('Dashboard:login_user'))

    account_email = request.user.username

    if connection.is_connected():
        cursor = connection.cursor()
        query = "UPDATE missing_person_info SET is_found=1 where " + \
                "identifier=%s and account_email='%s'" % (search_id, account_email)

        log(query)
        cursor.execute(query)
        result = cursor.fetchall()
        connection.commit()
        print(result)

def home(request):
    return render(request, 'Dashboard/index.html', context=None, content_type=None, status=None, using=None)


def login_user(request):

    error = request.session['error'] = ''
    is_found = request.session['is_found'] = False
    show_popup = request.session['no_match'] = False

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

    error = request.session['error'] = ''
    is_found = request.session['is_found'] = False
    show_popup = request.session['no_match'] = False

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('Dashboard:login_user'))

    return render(request, 'Dashboard/dashboard.html')


def upload(request, fileinput='fileinput'):
    img = request.FILES.get(fileinput)
    img_extension = os.path.splitext(img.name)[1]
    user_folder = os.path.join(settings.MEDIA_ROOT, str(request.user.id))
    if not os.path.exists(user_folder):
        os.mkdir(user_folder)
    epoch_seconds = time.time()
    print(epoch_seconds)
    avatar = 'avatar' + str(int(epoch_seconds)) + img_extension
    img_save_path = os.path.join(user_folder, avatar)
    with open(img_save_path, 'wb+') as f:
        for chunk in img.chunks():
            f.write(chunk)

    avatar = '/media/' + str(request.user.id) + '/' + avatar

    return avatar


def add_person(request):

    error = request.session['error'] = ''
    is_found = request.session['is_found'] = False
    show_popup = request.session['no_match'] = False

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('Dashboard:login_user'))

    if request.method == "POST":

        # missing person info
        fullname = request.POST['fullname']
        age = request.POST['age']
        img_save_path = upload(request)

        log(img_save_path)

        # guardian info
        guardian_name = request.POST['guardian_name']
        guardian_address = request.POST['guardian_address']
        guardian_contact = request.POST['guardian_contact']
        guardian_email = request.POST['guardian_email']
        is_found = False
        account_email = request.user.username
        if connection.is_connected():
            cursor = connection.cursor()
            query = "insert into missing_person_info " + \
                    "(name, age, imagename, guardian_name, guardian_address, guardian_contact, guardian_email, " \
                    "account_email, is_found) " + \
                    "VALUES('%s','%s','%s','%s','%s','%s','%s','%s',%s)" % (fullname, age, img_save_path, guardian_name,
                                                                            guardian_address, guardian_contact,
                                                                            guardian_email, account_email, is_found)
            log(query)
            cursor.execute(query)

            connection.commit()

            return HttpResponseRedirect(reverse('Dashboard:dashboard'))

    return render(request, "Dashboard/add_person.html")

def delete_person(request, userid):

    error = request.session['error'] = ''
    is_found = request.session['is_found'] = False
    show_popup = request.session['no_match'] = False

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('Dashboard:login_user'))
    if request.method == "POST":
        account_email = request.user.username
        if connection.is_connected():
            cursor = connection.cursor()
            query = "delete from missing_person_info where " + \
                    "identifier=%s and account_email='%s'" % (userid, account_email)

            log(query)
            cursor.execute(query)
            result = cursor.fetchall()
            connection.commit()
            print(result)

    return HttpResponseRedirect(reverse('Dashboard:dashboard'))

def search_person(request):

    error = request.session['error'] = ''
    is_found = request.session['is_found'] = False
    show_popup = request.session['no_match'] = False

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('Dashboard:login_user'))

    account_email = request.user.username
    # if username == 'admin':

    if request.method == "POST":
        search_id = request.POST['search_id']
        log(search_id)

        if connection.is_connected():
            cursor = connection.cursor()
            query = "select * from missing_person_info where " + \
                    "identifier=%s and account_email='%s'" % (search_id, account_email)

            log(query)
            cursor.execute(query)
            result = cursor.fetchall()
            connection.commit()
            print(result)

    elif account_email == 'admin@missingly.com':
        if connection.is_connected():
            cursor = connection.cursor()
            query = "select * from missing_person_info"
            log(query)
            cursor.execute(query)
            result = cursor.fetchall()
            connection.commit()
            print(result)

    else:
        if connection.is_connected():
            cursor = connection.cursor()
            username = request.user.username
            print(username)
            query = "select * from missing_person_info where " + \
                    "account_email='%s'" % username
            log(query)
            cursor.execute(query)
            result = cursor.fetchall()
            connection.commit()
            print(result)

    return render(request, "Dashboard/search.html", {'all_person': result})


def view_info(request, user_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('Dashboard:login'))

    if connection.is_connected():
        cursor = connection.cursor()
        query = "select * from missing_person_info where " + \
                "identifier=%s" % user_id

        log(query)
        cursor.execute(query)
        result = cursor.fetchall()
        connection.commit()
        print(result)
    if request.session.has_key('error'):
        log("has key error")
        error = request.session.get('error')
        is_found = request.session.get('is_found')
        show_popup = request.session.get('show_popup')

        return render(request, "Dashboard/view.html", {'person': result[0], 'error': error, 'is_found': is_found, 'show_popup': show_popup})

    return render(request, "Dashboard/view.html", {'person': result[0]})

def username_exists(username):
    if User.objects.filter(username=username).exists():
        return True
    else:
        return False

def register(request):

    error = request.session['error'] = ''
    is_found = request.session['is_found'] = False
    show_popup = request.session['no_match'] = False

    if request.method == "POST":
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if username == 'admin@missingly.com':
            return render(request, 'Dashboard/register.html', {'error_message': 'This email is already taken.'})

        if password1 != password2:
            return render(request, 'Dashboard/register.html', {'error_message': 'Your Passwords did not match.'})

        firstname = request.POST['firstname']
        lastname = request.POST['lastname']

        if username_exists(username):
            return render(request, 'Dashboard/register.html', {'error_message': 'Username already exists.'})

        if connection.is_connected():
            cursor = connection.cursor()
            query = "insert into registration_info " + \
                    "(firstname, lastname, email, password) " + \
                    "VALUES('%s','%s','%s','%s')" % (firstname, lastname, username, password1)
            log(query)
            cursor.execute(query)

            connection.commit()
            print (username)
            print (password1)
            user = User.objects.create_user(username=username, password=password1)
            user.save()

        else:
            return render(request, 'Dashboard/register.html', {'error_message': 'Issue in DB connection.'})
        return HttpResponseRedirect(reverse('Dashboard:login_user'))
    return render(request, "Dashboard/register.html")
