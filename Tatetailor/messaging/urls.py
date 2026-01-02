from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('chat/', views.chat, name='chat'),
    path('send/<str:room_name>/', views.send_message, name='send_message'),
    path('last-message/', views.get_last_message_data, name='api-last-message'),
    path('updates/', views.updates_list, name='updates_list'),
    path('updates/post/', views.post_update, name='post_update'),
    path('updates/edit/<int:update_id>/', views.edit_update, name='edit_update'),
    path('updates/delete/<int:update_id>/', views.delete_update, name='delete_update'),
    path('updates/<int:update_id>/react/', views.react_to_update, name='react_to_update'),
    path('updates/<int:update_id>/comment/', views.post_comment, name='post_comment'),
    path('comments/<int:comment_id>/like/', views.like_comment, name='like_comment'),     

    path('clear-chat/<str:room_name>/', views.clear_chat, name='clear_chat'),  
]
