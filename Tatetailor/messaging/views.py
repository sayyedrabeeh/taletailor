from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Message, ChatRoom
from authentication.models import Profile

def chat(request):
    users = User.objects.exclude(id=request.user.id)

    # Prepare chat list data
    for user in users:
        room = ChatRoom.objects.filter(participants=request.user).filter(participants=user).first()

        if room:
            last_msg = Message.objects.filter(room=room).order_by('-timestamp').first()
            last_message = last_msg.content if last_msg else "Start a conversation..."
            last_seen1 = last_msg.timestamp if last_msg else None
            unread_count = 0  # Placeholder
        else:
            last_message = "Start a conversation..."
            last_seen1 = None
            unread_count = 0

        # Attach chat preview info to each user
        user.last_message = last_message
        user.last_seen1 = last_seen1
        user.unread_count = unread_count

        # Get or create profile
        try:
            profile = user.profile
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=user)
        user.profile = profile
        user.is_online = profile.is_online()

    # If a specific room is requested, load it
    room = None
    messages = []
    room_name = request.GET.get('room_name')
    if room_name:
        room = get_object_or_404(ChatRoom, name=room_name)
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
