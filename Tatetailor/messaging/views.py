from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Q, Count
from .models import Message, ChatRoom

# Create your views here.
def chat_room(request, room_name):
    return render(request, 'chat.html', {
        'room_name': room_name
    })

def chat(request):
    users = User.objects.exclude(id=request.user.id)

    for user in users:
        room = ChatRoom.objects.filter(participants=request.user).filter(participants=user).distinct().first()
        
        if room:
            last_msg = Message.objects.filter(room=room).order_by('-timestamp').first()
            last_message = last_msg.content if last_msg else "Start a conversation..."
            last_seen = last_msg.timestamp if last_msg else None
            unread_count = 0  # Placeholder
        else:
            last_message = "Start a conversation..."
            last_seen = None
            unread_count = 0

        # Add these attributes to user directly (not user.profile)
        user.last_message = last_message
        user.last_seen = last_seen
        user.unread_count = unread_count

    return render(request, 'chatroom.html', {
        'users': users
    })