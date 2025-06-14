 
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

    class Meta:
        ordering = ['-created_at']