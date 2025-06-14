from django.apps import AppConfig


class MessagingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "messaging"

from django.apps import AppConfig

class MessagingConfig(AppConfig):
    name = 'messaging'

    def ready(self):
        import messaging.signals