from django.urls import path
# from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'Summaryapp'

urlpatterns = [
    path('', views.summary, name='summary'),
    path('result2/', views.result2, name='result2'),
    path('download/', views.downloadFile, name='downloadFile'),
    path('translate/', views.translate, name='translate'),
    path('enkr/',views.enkr,name='enkr'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)