from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from cloudinary.models import CloudinaryField

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = CloudinaryField('profile_picture',blank=True,null=True)
    bio = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address=models.TextField(blank=True, null=True)
    last_seen = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    def is_online(self):
        if self.last_seen:
            now = timezone.now()
            return now - self.last_seen <= timedelta(minutes=1)
        return False

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()