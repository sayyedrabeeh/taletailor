from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Message, ChatRoom
from authentication.models import Profile

 

def chat(request):
    users = User.objects.exclude(id=request.user.id)

    for user in users:
        room_name = f"room-{min(request.user.id, user.id)}-{max(request.user.id, user.id)}"
        room = ChatRoom.objects.filter(name=room_name).first()

        if not room:
            room = ChatRoom.objects.create(name=room_name)
            room.participants.set([request.user, user])

        last_msg = Message.objects.filter(room=room).order_by('-timestamp').first()
        last_message = last_msg.content if last_msg else "Start a conversation..."
        last_seen1 = last_msg.timestamp if last_msg else None
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
        room = ChatRoom.objects.filter(name=selected_room_name).first()
        if not room:

            parts = selected_room_name.split('-')
            if len(parts) == 3:
                _, uid1, uid2 = parts
                try:
                    user1 = User.objects.get(id=int(uid1))
                    user2 = User.objects.get(id=int(uid2))
                    room = ChatRoom.objects.create(name=selected_room_name)
                    room.participants.set([user1, user2])
                except:
                    room = None 
        if room:
            messages = Message.objects.filter(room=room).order_by('timestamp')

    return render(request, 'chatroom.html', {
        'users': users,
        'room': room,
        'room_name': room.name if room else None,
        'messages': messages,
    })

def send_message(request, room_name):
    print('hii')
    if request.method == 'POST':
        print('post:',room_name)
        content = request.POST.get('content')
        if content:
            room = get_object_or_404(ChatRoom, name=room_name)
            Message.objects.create(
                room=room,
                sender=request.user,
                content=content
            )
    return redirect(f'/messaging/chat/?room_name={room_name}')
