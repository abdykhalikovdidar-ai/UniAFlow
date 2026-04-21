import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import название_твоего_приложения.routing 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kanban_system.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            название_твоего_приложения.routing.websocket_urlpatterns
        )
    ),
})