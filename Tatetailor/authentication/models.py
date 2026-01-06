from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from cloudinary.models import CloudinaryField
from django.db import IntegrityError

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
    """Create or get profile for user - handles duplicates gracefully"""
    try:
        
        profile, created_profile = Profile.objects.get_or_create(user=instance)
        if created_profile:
            print(f"✅ Created profile for user: {instance.username}")
        else:
            print(f"ℹ️ Profile already exists for user: {instance.username}")
    except IntegrityError as e:
        
        print(f"⚠️ IntegrityError when creating profile: {e}")
        try:
            profile = Profile.objects.get(user=instance)
            print(f"ℹ️ Retrieved existing profile for user: {instance.username}")
        except Profile.DoesNotExist:
            print(f"❌ Could not create or retrieve profile for user: {instance.username}")