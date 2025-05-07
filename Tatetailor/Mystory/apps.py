from django.apps import AppConfig


class MystoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Mystory'

    def ready(self):
        import Mystory.signals   
