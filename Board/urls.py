from django.urls import path
from . import views

app_name='Board'
urlpatterns = [
    path('write/',views.board_write,name='board_write'),
    path('reading/board/<int:b_no>',views.detail_board,name='detail_board'),
    path('board_list/',views.board_list,name='board_list'),
]
