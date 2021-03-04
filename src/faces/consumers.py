import json

from django.conf import settings

from channels.generic.websocket import AsyncWebsocketConsumer


class Consumer(AsyncWebsocketConsumer):

    async def connect(self):
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(json.dumps(message))


class NotificationConsumer(Consumer):
    """Notification ws consumer."""
    room_group_name = settings.ROOM_NAME_NOTIFICATIONS


class FaceConsumer(Consumer):
    """Notification ws consumer."""
    room_group_name = settings.ROOM_NAME_FACES
