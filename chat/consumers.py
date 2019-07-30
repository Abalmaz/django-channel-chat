import json
from channels.generic.websocket import AsyncConsumer
from channels.db import database_sync_to_async

from chat.models import Room, ChatMessage


class ChatConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        scope_room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_obj = await self.get_room(scope_room_name)
        self.chat_room = self.room_obj.group_name
        user = self.scope['user']
        self.username = user.username if user.is_authenticated else 'anonymous'

        # Join room group
        await self.channel_layer.group_add(
            self.chat_room,
            self.channel_name
        )

        await self.send({
            "type": "websocket.accept"
        })

    async def websocket_disconnect(self, event):
        # print("disconnect", event)
        # Leave room group
        await self.channel_layer.group_discard(
            self.chat_room,
            self.channel_name
        )

    # Receive message from WebSocket
    async def websocket_receive(self, event):

        handlers = {
            'send': self.send_msg,
            'typing': self.typing_msg
        }

        message = event.get('text', None)
        text_data_json = json.loads(message)
        self.msg = text_data_json.get('message', None)
        command = text_data_json.get('command', None)
        handler = handlers[command]
        await handler()

    async def chat_message(self, event):
        await self.send({
            "type": "websocket.send",
            "text": event['text']
        })

    @database_sync_to_async
    def get_room(self, room_name):
        return Room.objects.get_or_new(room_name)

    @database_sync_to_async
    def create_chat_msg(self, user):
        return ChatMessage.objects.create(room=self.room_obj,
                                          user=user,
                                          message=self.msg)

    async def send_msg(self):
        user = self.scope['user']
        await self.create_chat_msg(user)
        await self.channel_layer.group_send(
            self.chat_room,
            {
                "type": "chat_message",
                "text": json.dumps({
                    'message': self.msg,
                    'username': self.username,
                    'event': 'send'
                })
            }
        )

    async def typing_msg(self):
        await self.channel_layer.group_send(
            self.chat_room,
            {
                "type": "chat_message",
                "text": json.dumps({
                    'username': self.username,
                    'event': 'is_typing'
                })
            }
        )
