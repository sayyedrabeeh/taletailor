from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.

class Story(models.Model):
    STATUS_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="stories")
    collaborators = models.ManyToManyField(User, related_name="collaborations", blank=True)
    image = models.ImageField(upload_to='story_images/', null=True, blank=True)

    title = models.CharField(max_length=100)
    content = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, blank=True,null=True )  
    is_collaborated = models.BooleanField(default=False)
    is_ai_generated = models.BooleanField(default=False)

    length = models.CharField(
        max_length=10, 
        choices=[("short", "Short"), ("medium", "Medium"), ("long", "Long")], 
        default='medium'
    )
    GENRE_CHOICES = [
    ('mystery', 'Mystery'),
    ('romance', 'Romance'),
    ('fantasy', 'Fantasy'),
    ('horror', 'Horror'),
     
]

    genre = models.CharField(max_length=50, choices=GENRE_CHOICES, blank=True, null=True)
    emotions = models.CharField(max_length=255, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def is_collaborator(self, user):
        """Check if the user is the owner or a collaborator."""
        return user == self.user or self.collaborators.filter(id=user.id).exists()

    def add_collaborator(self, user):
        """Add a collaborator and update the story status."""
        self.collaborators.add(user)
        self.is_collaborated = True
        self.save()

class StoryView(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)

class StoryLike(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CollaborationInvite(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="collaboration_invites",null=True, blank=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_invites")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_invites")

    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')],
        default='pending'
    )

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} → {self.receiver} ({self.status}) on {self.story.title}"

    def accept(self):
        """Accepts the invite and adds the receiver as a collaborator."""
        self.status = "accepted"
        self.save()
        self.story.add_collaborator(self.receiver)

    def reject(self):
        """Rejects the invite."""
        self.status = "rejected"
        self.save()

class Follower(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Update(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return self.created_at < timezone.now() - timedelta(hours=24)

    def __str__(self):
        return f"{self.user.username} - {self.content[:20]}"