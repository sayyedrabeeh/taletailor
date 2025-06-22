# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class StoryEditorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"story_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        await self.send(text_data=json.dumps({"type": "connected", "message": "WebSocket connected"}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        content = data["content"]
        title = data.get("title")

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "broadcast_edit",
                "content": content,
                "title": title,
            }
        )

    async def broadcast_edit(self, event):
        await self.send(text_data=json.dumps({
            "content": event["content"],
            "title": event.get("title", ""),
        }))
