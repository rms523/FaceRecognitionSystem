from django.urls import path
from . import views

# app_name to set application namespace.
app_name = 'Dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('login_user', views.login_user, name='login_user'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('register', views.register, name='register'),
    path('search_person', views.search_person, name='search_person'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('add_person', views.add_person, name='add_person'),
    path('view_info', views.view_info, name='view_info'),

]
