from xml.etree.ElementInclude import include
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name='Board'

urlpatterns = [
    path('Board/writing/',views.writing,name='writing')
]
