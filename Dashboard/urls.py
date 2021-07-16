from django.urls import path, re_path
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
    path('delete_person/<int:userid>', views.delete_person, name='delete_person'),
    re_path('^view_info/(?P<user_id>\d{5,9})/$', views.view_info, name='view_info'),

]
