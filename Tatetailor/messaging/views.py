from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Message, ChatRoom
from authentication.models import Profile

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import Message, ChatRoom
from authentication.models import Profile

def chat(request):
    users = User.objects.exclude(id=request.user.id)

    for user in users:
        room_name = f"room-{min(request.user.id, user.id)}-{max(request.user.id, user.id)}"
        room = ChatRoom.objects.filter(name=room_name).first()
        
        if room:
            last_msg = Message.objects.filter(room=room).order_by('-timestamp').first()
            last_message = last_msg.content if last_msg else "Start a conversation..."
            last_seen1 = last_msg.timestamp if last_msg else None
            unread_count = 0  
        else:
            last_message = "Start a conversation..."
            last_seen1 = None
            unread_count = 0

        
        user.last_message = last_message
        user.last_seen1 = last_seen1
        user.unread_count = unread_count
        user.chatroom_name = room_name   

 
        try:
            profile = user.profile
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=user)
        user.profile = profile
        user.is_online = profile.is_online()

     
    room = None
    messages = []
    selected_room_name = request.GET.get('room_name')

    if selected_room_name:
        room = get_object_or_404(ChatRoom, name=selected_room_name)
        messages = Message.objects.filter(room=room).order_by('timestamp')

    return render(request, 'chatroom.html', {
        'users': users,
        'room': room,
        'room_name': room.name if room else None,
        'messages': messages,
    })


def send_message(request, room_name):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            room = get_object_or_404(ChatRoom, name=room_name)
            Message.objects.create(
                room=room,
                sender=request.user,
                content=content
            )
    return redirect(f'/messaging/chat/?room_name={room_name}')
