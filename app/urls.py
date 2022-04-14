from django.urls import path, include
from . import views

app_name = 'app'

urlpatterns = [
    path('index/', views.index),
    path('login/', views.login),
    path('register/', views.register),
    path('password/', views.password),
]
#