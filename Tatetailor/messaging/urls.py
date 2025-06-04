 
from django.contrib import admin
from django.urls import path 
from .views import chat_room,chat,send_message

app_name = 'messaging' 

urlpatterns = [
   
   path('chat/', chat, name='chat'),
    path('chat/<str:room_name>/', chat_room, name='chat_room'),
    path('chat/<str:room_name>/send/', send_message, name='send_message'),
   
]

    
    
