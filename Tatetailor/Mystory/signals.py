# Mystory/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Story, Follower, Notification

@receiver(post_save, sender=Story)
def notify_followers_on_story(sender, instance, created, **kwargs):
    if created and instance.status == 'public':
        followers = Follower.objects.filter(following=instance.user)
        for f in followers:
            Notification.objects.create(
                user=f.follower,
                message=f"{instance.user.username} just posted a new story: '{instance.title}'"
            )
