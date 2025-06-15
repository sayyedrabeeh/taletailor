from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        if not self.channel_layer:
             print("❌ No channel layer configured!")
             await self.close()
             return
       
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        
        await self.accept()

    async def disconnect(self, close_code):
        # ✅ Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        username = data.get("username", "Anonymous")

        # ✅ Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username,
                'room_name': self.room_name 
            }
        )

    async def chat_metadata(self, event):
       await self.send(text_data=json.dumps({
        "type": "metadata",
        "chat": event["chat"]
    }))


    async def chat_message(self, event):
        message = event["message"]
        username = event.get("username", "Anonymous")
        room_name = event.get("room_name")

        # ✅ Send message to WebSocket
        await self.send(text_data=json.dumps({
            "message": message,
            "username": username,
            'room_name': room_name
        }))


