 
from django.contrib import admin
from django.urls import path 
from .views import chat_room,chat

app_name = 'messaging' 

urlpatterns = [
   path('chat/<str:room_name>/', chat_room, name='chat_room'),
   path('chat/', chat, name='chat'),
   
]

    
    
