import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tatetailor.settings')

from django.core.asgi import get_asgi_application
application = get_asgi_application()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import messaging.routing

application = ProtocolTypeRouter({
    "http": application,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            messaging.routing.websocket_urlpatterns
        )
    ),
})
