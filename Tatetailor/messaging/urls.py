from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('chat/', views.chat, name='chat'),
    path('send/<str:room_name>/', views.send_message, name='send_message'),
]
