from django.urls import path
from . import views

app_name = 'Searchapp'

urlpatterns = [
    path('category/', views.category, name='category'),
    path('booksearch/', views.booksearch, name='booksearch'),
    path('book/', views.book, name='book'),
    path('document/', views.document, name = 'document'),
    path('documentsearch/', views.documentsearch, name = 'documentsearch'),
]  