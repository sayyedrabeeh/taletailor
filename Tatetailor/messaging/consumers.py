import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatRoom, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope["user"]

        if self.user.is_anonymous:
            await self.close()
            return

        # Add the user to the room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Remove user from room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message")

        if not message:
            return  # Don't process empty messages

        username = self.user.username

        # Save the message to DB
        room = await self.get_room(self.room_name)
        await self.create_message(self.user, room, message)

        # Broadcast the message to everyone in the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username,
            }
        )

    # This is called by group_send → must match "type"
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "username": event["username"]
        }))

    @database_sync_to_async
    def get_room(self, name):
        return ChatRoom.objects.get(name=name)

    @database_sync_to_async
    def create_message(self, sender, room, content):
        return Message.objects.create(sender=sender, room=room, content=content)
