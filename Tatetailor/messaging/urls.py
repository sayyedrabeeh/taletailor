 
from django.contrib import admin
from django.urls import path 
from .views import chat_room

app_name = 'authentication' 

urlpatterns = [
   path('chat/<str:room_name>/', chat_room, name='chat_room'),
]

    
    
