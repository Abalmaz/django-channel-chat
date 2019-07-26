import json
from channels.generic.websocket import AsyncConsumer


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        await  self.send({
            "type": "websocket.accept"
        })

        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        # self.room_group_name = 'chat_%s' % self.room_name
        #
        # # Join room group
        # await self.channel_layer.group_add(
        #     self.room_group_name,
        #     self.channel_name
        # )
        #
        # await self.accept()

    async def websocket_disconnect(self, event):
        print("disconnect", event)
        # # Leave room group
        # await self.channel_layer.group_discard(
        #     self.room_group_name,
        #     self.channel_name
        # )

    # Receive message from WebSocket
    async def websocket_receive(self, event):
        message = event.get('text', None)
        text_data_json = json.loads(message)
        msg = text_data_json.get('message')
        user = self.scope['user']
        username = user.username if user.is_authenticated else 'anonymous'
        await self.send({
            "type": "websocket.send",
            "text": json.dumps({
                "message": msg,
                "username": username
            })
        })

        #
        # # Send message to room group
        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type': 'chat_message',
        #         'message': message
        #     }
        # )

    # Receive message from room group
    # async def chat_message(self, event):
    #     message = event['message']
    #
    #     # Send message to WebSocket
    #     await self.send(text_data=json.dumps({
    #         'message': message
    #     }))



