# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Story 

class StoryEditorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # Extract story ID from room_name (e.g., 'story-21')
        story_id = self.room_name.split('-')[-1]

        try:
            story = await sync_to_async(Story.objects.get)(id=story_id)
            await self.send(text_data=json.dumps({
                "type": "initial",
                "title": story.title,
                "content": story.content
            }))
        except Story.DoesNotExist:
            await self.send(text_data=json.dumps({
                "type": "error",
                "message": "Story not found"
            }))

        await self.send(text_data=json.dumps({"type": "connected", "message": "WebSocket connected"}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        content = data.get("content", "")
        title = data.get("title", "")

        story_id = self.room_name.split('-')[-1]

        # Save to DB
        try:
            story = await sync_to_async(Story.objects.get)(id=story_id)
            story.title = title
            story.content = content
            await sync_to_async(story.save)()
        except Story.DoesNotExist:
            pass

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
            "type": "broadcast_edit",
            "content": event["content"],
            "title": event.get("title", "")
        }))
