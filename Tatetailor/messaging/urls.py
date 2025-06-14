from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('chat/', views.chat, name='chat'),
    path('send/<str:room_name>/', views.send_message, name='send_message'),
    path('last-message/', views.get_last_message_data, name='api-last-message'),
    path('updates/', views.updates_list, name='updates_list'),
    path('updates/post/', views.post_update, name='post_update'),
]
