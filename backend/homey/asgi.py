import os
import django
from channels.http import AsgiHandler
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing
from homey.settings import base

if base.DEBUG==False:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homey.settings.prod')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homey.settings.local')

django.setup()

application = ProtocolTypeRouter({
  "http": AsgiHandler(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),

})
