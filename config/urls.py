"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# from mysite.views import HomeView
# from mysite.views import UserCreateView, UserCreateDoneTV
from django.conf import settings
from django.conf.urls.static import static
from meeting.views import audio


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('Mainapp.urls')),
    path('search/', include('Searchapp.urls')),
    path('summary/', include('Summaryapp.urls')),
    # path('', HomeView.as_view(), name='home'),
    path('summernote/',include('django_summernote.urls')),
    path('Board/',include('Board.urls')),
    path('meeting/',include('meeting.urls', namespace='meeting')),
    path(r'', audio),


   
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

