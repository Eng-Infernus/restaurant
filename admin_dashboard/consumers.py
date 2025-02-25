#admin_dashboard / consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer


class OrderNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if not self.scope["user"].is_staff:
            await self.close()
            return

        await self.channel_layer.group_add("admin_notifications", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("admin_notifications", self.channel_name)

    async def notify_order(self, event):
        # Make sure the message matches exactly what we're sending
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))
