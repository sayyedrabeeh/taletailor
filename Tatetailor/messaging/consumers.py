# messaging/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatRoom, Message
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope["user"]

        if self.user.is_anonymous:
            await self.close(code=4001)
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        print(f"🔌 Disconnected from {self.room_name} with code: {close_code}")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
      try:
        data = json.loads(text_data)
        message = data.get("message", "").strip()
        username = data.get("username", "")

        if not message:
            return  # Do not send empty messages

        room = await self.get_room(self.room_name)
        await self.create_message(self.user, room, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )
      except Exception as e:
        print("WebSocket receive error:", e)
        # Don't raise error – just log


    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))

    @database_sync_to_async
    def get_room(self, room_name):
        return ChatRoom.objects.get(name=room_name)

    @database_sync_to_async
    def create_message(self, sender, room, content):
        return Message.objects.create(sender=sender, room=room, content=content)
