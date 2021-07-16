from django.urls import path, re_path
from . import views

# app_name to set application namespace.
app_name = 'FaceApp'

urlpatterns = [
    path('processImage/<path:imagesavepath>/<int:user_id>/', views.processImage, name='processImage'),
    # path('processImage/',views.processImage, name='processImage'),
    path('webStream/', views.webStream, name='webStream'),
]