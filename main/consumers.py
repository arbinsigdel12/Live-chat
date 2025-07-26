from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
import json
from .models import PrivateMessage, PrivateChatRoom, Message
from django.contrib.auth.models import User
from django.templatetags.static import static

# ----- PUBLIC CHAT CONSUMER -----
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'public'
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        user = self.scope['user']

        if user.is_authenticated:
            name, username, image = await self.get_user_data(user)
            await sync_to_async(Message.objects.create)(user=user, content=message)
        else:
            name, username, image = 'Anonymous', 'anonymous', '/static/images/default.png'

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'name': name,
                'username': username,
                'image': image
            }
        )

    @sync_to_async
    def get_user_data(self, user):
        profile = user.profile
        return (
            profile.name or user.username,
            user.username,
            profile.image.url if profile.image else '/static/images/default.png'
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'name': event['name'],
            'username': event['username'],
            'image': event['image']
        }))


# ----- PRIVATE CHAT CONSUMER -----
class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'private_chat_{self.room_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        user = self.scope['user']

        await self.save_message(user, self.room_id, message)
        name, image = await self.get_user_display_and_image(user)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message_private',
                'message': message,
                'username': user.username,
                'name': name,
                'image': image,
            }
        )

    async def chat_message_private(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
            'name': event['name'],
            'image': event['image'],
        }))

    @sync_to_async
    def save_message(self, user, room_id, message):
        room = PrivateChatRoom.objects.get(id=room_id)
        return PrivateMessage.objects.create(user=user, room=room, content=message)

    @sync_to_async
    def get_user_image_url(self, user):
        profile = user.profile
        if profile.photo:
            return profile.photo.url
        return '/static/images/default.png'
    
    @database_sync_to_async
    def get_user_display_and_image(self, user):
        try:
            if hasattr(user, 'profile') and user.profile.image:
                return user.username, user.profile.image.url
        except:
            pass
        return user.username, static('images/default.png')   