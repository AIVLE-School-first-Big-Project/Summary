from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'Summaryapp'

urlpatterns = [
    path('', views.summary, name='summary'),
    path('text/', views.text, name = 'text'),
    path('textsummary/', views.textsummary, name = 'textsummary'),
    path('result2/', views.result2, name = 'result2'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)