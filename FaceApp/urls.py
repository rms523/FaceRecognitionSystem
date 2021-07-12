from django.urls import path
from . import views

# app_name to set application namespace.
app_name = 'FaceApp'

urlpatterns = [
    path('processImage/', views.processImage, name='processImage'),
    path('webStream/', views.webStream, name='webStream'),
]