from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'Mainapp'

urlpatterns = [
    path('', views.main, name='main'),
    # path('search/', views.search_category, name='search_category'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('mypage/', views.mypage, name='mypage'),
    
    # path('login/',
    #     auth_views.LoginView.as_view(template_name='Main/login.html'),
    #     name='login'
    #     ),

    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
        
    # path('signup/', views.signup, name='signup'),

    # path('profile_update/', views.profile_update, name='profile_update'),

    
]  
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)