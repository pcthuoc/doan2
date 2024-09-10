from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json

class NotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.group_name = 'notifications'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        print("Received message from client:", message)
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'send_notification',
                'message': message
            }
        )


    async def send_notification(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))

class RelayConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.group_name = 'updates'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_update(self, event):
        pin = event['pin']
        value = event['value']
        await self.send(text_data=json.dumps({
            pin: value
        }))

class SensorConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.group_name = 'updates'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_update(self, event):
        pin = event['pin']
        value = event['value']
        await self.send(text_data=json.dumps({
            pin: value
        }))
