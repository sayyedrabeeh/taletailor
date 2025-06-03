from django.shortcuts import render
from django.contrib.auth.models import User


# Create your views here.
def chat_room(request, room_name):
    return render(request, 'chat.html', {
        'room_name': room_name
    })

def chat(request):
    users= User.objects.all()
    return render(request, 'chatroom.html',{
        'users': users
    })