from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('user/<str:username>/', views.user_profile, name='user_profile'),
    path('photo/<int:photo_id>/', views.photo_detail, name='photo_detail'),
    path('upload/', views.upload_photo, name='upload_photo'),
    path('my-photos/', views.my_photos, name='my_photos'),
    path('photo/<int:photo_id>/edit/', views.edit_photo, name='edit_photo'),
    path('photo/<int:photo_id>/delete/', views.delete_photo, name='delete_photo'),
    path('photo/<int:photo_id>/download/', views.download_photo, name='download_photo'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),

    path('tictactoe/', views.tic_tac_toe_list, name='tic_tac_toe_list'),
    path('tictactoe/<int:game_id>/', views.tic_tac_toe_detail, name='tic_tac_toe_detail'),
    path('tictactoe/<int:game_id>/move/<int:cell_index>/', views.tic_tac_toe_move, name='tic_tac_toe_move'),
    path('tictactoe/<int:game_id>/delete/', views.tic_tac_toe_delete, name='tic_tac_toe_delete'),
    path('tictactoe/<int:game_id>/end/', views.tic_tac_toe_end, name='tic_tac_toe_end'),
]