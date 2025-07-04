from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Message, ChatRoom
from authentication.models import Profile
from django.http import JsonResponse
from django.contrib import messages
from .models import Update,Reaction,Comment,CommentLike
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta

 
def chat(request):
    users = User.objects.exclude(id=request.user.id).select_related('profile')
    if not request.user.is_authenticated or request.user.id is None:
        return redirect('authentication:login')
    for user in users:
        try:
            profile = user.profile
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=user)
        
        room_name = f"room-{min(request.user.id, user.id)}-{max(request.user.id, user.id)}"
        room = ChatRoom.objects.filter(name=room_name).first()

        if not room:
            room = ChatRoom.objects.create(name=room_name)
            room.participants.set([request.user, user])

        last_msg = Message.objects.filter(room=room).order_by('-timestamp').first()
        user.last_seen1 = last_msg.timestamp if last_msg else None
        user.chatroom_name = room_name
        user.profile = profile
        user.is_online = profile.is_online()
        user.last_seen = profile.last_seen

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
            unread_messages = messages.exclude(read_by=request.user).exclude(sender=request.user)
            for msg in unread_messages:
                msg.read_by.add(request.user)

            for participant in room.participants.all():
                if participant != request.user:
                    try:
                        profile = participant.profile
                    except Profile.DoesNotExist:
                        profile = Profile.objects.create(user=participant)

                    participant.is_online = profile.is_online()
                    participant.last_seen = profile.last_seen

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


def get_last_message_data(request):
    user = request.user
    data = []

    # Get all rooms the user is part of
    rooms = ChatRoom.objects.filter(participants=user)

    for room in rooms:
        other_user = room.participants.exclude(id=user.id).first()

        last_msg = Message.objects.filter(room=room).order_by("-timestamp").first()
        last_message = last_msg.content if last_msg else "Start a conversation..."
        timestamp = last_msg.timestamp.isoformat() if last_msg else None

        unread_count = Message.objects.filter(
            room=room
        ).exclude(sender=user).exclude(read_by=user).count()

        data.append({
            "room_name": room.name,
            "other_user_id": other_user.id if other_user else None,
            "last_message": last_message,
            "timestamp": timestamp,
            "unread_count": unread_count,
        })

    return JsonResponse({"chats": data})

@login_required
def updates_list(request):
    updates = Update.objects.filter(created_at__gte=timezone.now() - timezone.timedelta(hours=24))
    for update in updates:
        update.top_level_comments = update.comments.filter(parent__isnull=True)

    return render(request, 'updates_list.html', {'updates': updates})



@login_required
def post_update(request):
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Update.objects.create(user=request.user, text=content)
        return redirect('messaging:updates_list')
    return render(request, 'post_update.html')


@login_required
def edit_update(request, update_id):
    update = get_object_or_404(Update, id=update_id, user=request.user)
    if request.method == 'POST':
        new_text = request.POST.get('content', '').strip()
        if new_text:
            update.text = new_text
            update.save()
            messages.success(request, "Update successfully edited!")
        return redirect('messaging:updates_list')
    return render(request, 'post_update.html', {'update': update})


@login_required
def delete_update(request, update_id):
    update = get_object_or_404(Update, id=update_id, user=request.user)
    if request.method == 'POST':
        update.delete()
        messages.success(request, 'Your update was deleted.')
    return redirect('messaging:updates_list')



@login_required
def react_to_update(request, update_id):
    update = get_object_or_404(Update, id=update_id)
    reaction_type = request.POST.get('reaction_type')

    if reaction_type in ['like', 'dislike']:
        Reaction.objects.update_or_create(
            user=request.user,
            update=update,
            defaults={'reaction_type': reaction_type}
        )
    return JsonResponse({
        'likes_count': update.likes_count(),
        'dislikes_count': update.dislikes_count()
    })



@login_required
def post_comment(request, update_id):
    if request.method == 'POST':
        update = get_object_or_404(Update, id=update_id)
        text = request.POST.get('text', '').strip()
        parent_id = request.POST.get('parent_id')

        if not text:
            return JsonResponse({'error': 'Comment cannot be empty'}, status=400)

        parent = Comment.objects.filter(id=parent_id).first() if parent_id else None
        comment = Comment.objects.create(user=request.user, update=update, text=text, parent=parent)

        return JsonResponse({
            'message': 'Comment created successfully',
            'comment': {
                'id': comment.id,
                'username': request.user.username.split('@')[0],
                'text': comment.text,
                'created_at_iso': comment.created_at.isoformat(),
                'like_count': comment.like_count(),
                'parent_id': parent.id if parent else None
            }
        })

    return JsonResponse({'error': 'Invalid request method'}, status=405)



@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    like, created = CommentLike.objects.get_or_create(user=request.user, comment=comment)
    if not created:
        like.delete()
    return JsonResponse({'like_count': comment.like_count()})