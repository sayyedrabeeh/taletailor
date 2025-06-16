 
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class ChatRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    participants = models.ManyToManyField(User)

    def __str__(self):
        return self.name


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    audio = models.FileField(upload_to="audio/", blank=True, null=True)  
    read_by = models.ManyToManyField(User, related_name='read_messages', blank=True)

    def __str__(self):
        return f"From {self.sender.username} in {self.room.name}"


    class Meta:
        ordering = ['-timestamp'] 



 
class Update(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="updates")
    text = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(hours=24)


    def likes_count(self):
        return self.reactions.filter(reaction_type='like').count()

    def dislikes_count(self):
        return self.reactions.filter(reaction_type='dislike').count()

    def comments_count(self):
        return self.comments.count()

    class Meta:
        ordering = ['-created_at']



class Reaction(models.Model):
    REACTION_CHOICES = [
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    update = models.ForeignKey(Update, on_delete=models.CASCADE, related_name='reactions')
    reaction_type = models.CharField(max_length=7, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'update') 


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    update = models.ForeignKey(Update, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def is_reply(self):
        return self.parent is not None

    def like_count(self):
        return self.comment_likes.count()


class CommentLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'comment')