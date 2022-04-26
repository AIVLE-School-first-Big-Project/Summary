from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'Summaryapp'

urlpatterns = [
    # path('', views.main, name='main'),
    path('', views.summary, name='summary'),
    # path('login/', views.login, name='login'),
    # path('signup/', views.signup, name='signup'),
    
]  