"""ASGI entry-point for HTTP and WebSocket.

- HTTP is served by Django's ASGI application
- WebSockets are handled by Channels with authentication and allowed host checks
"""

import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter,URLRouter
import chatapp.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = ProtocolTypeRouter({
        'http': get_asgi_application(),
        'websocket': AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(
                    chatapp.routing.websocket_urlpatterns
                )
            )
        )
})
