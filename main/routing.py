from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'^ws/chat/$', consumers.ChatConsumer.as_asgi()),  
    re_path(r'^ws/chat/public/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/private_chat/(?P<room_id>\d+)/$', consumers.PrivateChatConsumer.as_asgi()),
]
