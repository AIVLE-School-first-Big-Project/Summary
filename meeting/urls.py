from django.urls import path
from . import views

app_name = 'meeting'

urlpatterns = [
    path('meetingstart/meeting', views.audio),
    # path('home', views.audio),
    path('meetingstart/', views.meetingstart, name='meetingstart'),


]