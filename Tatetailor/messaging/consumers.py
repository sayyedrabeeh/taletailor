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
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        username = data.get("username", "Anonymous")

        # ✅ Send to current room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username,
                "room_name": self.room_name,
            }
        )

        # ✅ Also notify receiver's personal group
    
        receiver_username = await self.get_receiver_username(self.room_name, username)

        await self.channel_layer.group_send(
            f"notify_{receiver_username}",
            {
                "type": "send_notification",
                "data": {
                    "room_name": self.room_name,
                    "message": message,
                    "username": username,
                }
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "username": event["username"],
            "room_name": event["room_name"],
        }))

    async def get_receiver_username(self, room_name, sender_username):
        """
        Dummy logic: split room name and return the other user.
        You should replace this with real DB logic if needed.
        Example: room_name = "alice_bob"
        """
        users = room_name.split("_")
        return users[1] if users[0] == sender_username else users[0]

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.username = self.scope["url_route"]["kwargs"]["username"]
        self.group_name = f"notify_{self.username}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        pass

    async def send_notification(self, event):
        await self.send(text_data=json.dumps(event["data"]))
