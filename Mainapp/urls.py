from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
# from django.conf import settings
# from django.conf.urls.static import static

app_name = 'Mainapp'

urlpatterns = [
    path('', views.main, name='main'),
    path('login/', auth_views.LoginView.as_view(template_name='Main/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),       
    path('signup/', views.signup, name='signup'),
    
    path('mypage/', views.mypage, name='mypage'),
    path('mypage/profile_update', views.profile_update, name='profile_update'),
    path('mypage/<str:table>', views.my_category, name='my_category'),
    path('mypage/search/', views.search, name='search'),

]  
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)