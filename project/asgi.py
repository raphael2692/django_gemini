import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from todo import routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns)),
    }
)