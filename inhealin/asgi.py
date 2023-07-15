import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
# from django.conf import settings
# settings.configure()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inhealin.settings')
django.setup()


django_application = get_asgi_application()

from cadmin.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
     'http': django_application,

     'websocket': AuthMiddlewareStack(
         URLRouter(
          websocket_urlpatterns
       )
      )

})


