from django.urls import path
from . import views

# app_name to set application namespace.
app_name = 'Dashboard'

# the 'name' value as called by the {% url %} template tag

urlpatterns = [
    path('', views.home, name='Home'),
    path('login', views.admin_login, name='Admin_Login'),
    path('dashboard', views.dashboard, name='Dashboard')

]