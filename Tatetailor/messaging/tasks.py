from celery import shared_task
from django.utils import timezone
from .models import Update
from datetime import timedelta

@shared_task
def delete_expired_updates():
    expiry_time = timezone.now() - timedelta(hours=24)
    count, _ = Update.objects.filter(created_at__lt=expiry_time).delete()
    return f"Deleted {count} expired updates"
