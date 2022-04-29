from django.urls import path
from . import views

app_name='Board'
urlpatterns = [
    path('write/',views.board_write,name='board_write'),
    path('reading/board/<int:b_no>',views.detail_board,name='detail_board'),
    path('board_list/',views.board_list,name='board_list'),
    path('write/update/<int:b_no>',views.update_board,name='update_board'),
    path('board/board_delete/<int:b_no>/',views.board_delete,name='board_delete'),
    path('board/comment/',views.comment,name='comment'),

    path('board/comment/delete/<int:b_no>/<int:r_no>', views.comment_delete,  name='comment_delete'),
    path('board/comment/update/<int:b_no>/<int:r_no>', views.comment_updateurl,  name='comment_updateurl'),
    path('board/comment/update/<int:r_no>', views.comment_update,  name='comment_update'),

    path('search/',views.search,name='search'),
]
