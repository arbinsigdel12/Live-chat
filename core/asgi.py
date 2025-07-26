import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()


from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from main.routing import websocket_urlpatterns

from starlette.staticfiles import StaticFiles
from starlette.routing import Mount
from starlette.applications import Starlette

# Django ASGI handler
django_asgi_app = get_asgi_application()

# Static/media via Starlette
starlette_app = Starlette(routes=[
    Mount('/static', StaticFiles(directory='static'), name='static'),
    Mount('/media', StaticFiles(directory='media'), name='media'),
    Mount('/', app=django_asgi_app),
])

# Final ASGI application
application = ProtocolTypeRouter({
    "http": starlette_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
