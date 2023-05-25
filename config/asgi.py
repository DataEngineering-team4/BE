"""
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

django_asgi_app = get_asgi_application()

if True:
    from core import routing


asgi_routes = {}
asgi_routes["http"] = django_asgi_app
asgi_routes["weboscket"] = AuthMiddlewareStack(
    URLRouter(routing.websocket_urlpatterns)
)
application = ProtocolTypeRouter(asgi_routes)
