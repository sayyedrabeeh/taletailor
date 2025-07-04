import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Story





class StoryEditorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = self.room_name

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

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

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)

        # Typing indicator
        if data.get("type") == "user_typing":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "user_typing_event",
                    "is_typing": data.get("is_typing", False),
                    "user_id": data.get("user_id"),
                    "username": data.get("username"),
                }
            )
            return

        # Save and broadcast edits
        story_id = self.room_name.split('-')[-1]
        try:
            story = await sync_to_async(Story.objects.get)(id=story_id)
        except Story.DoesNotExist:
            return

        user_id = data.get("user_id")
        story_owner_id = await sync_to_async(lambda s: s.user.id)(story)
        if story.status in ["public", "private"] and str(story_owner_id) != str(user_id):

            await self.send(text_data=json.dumps({
                "type": "error",
                "message": "Only the story owner can edit a published story."
            }))
            return

        content = data.get("content", "")
        title = data.get("title", "")

        story.title = title
        story.content = content
        await sync_to_async(story.save)()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "broadcast_edit",
                "content": content,
                "title": title,
            }
        )

    async def user_typing_event(self, event):
        await self.send(text_data=json.dumps({
            "type": "user_typing",
            "is_typing": event["is_typing"],
            "user_id": event["user_id"],
            "username": event["username"]  
        }))

    async def broadcast_edit(self, event):
        await self.send(text_data=json.dumps({
            "type": "broadcast_edit",
            "content": event["content"],
            "title": event.get("title", "")
        }))
