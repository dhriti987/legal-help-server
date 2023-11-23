import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from .models import MessageThread, Message
from .serializers import MessageThreadSerializer, MessageSerializer

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async

class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        if isinstance(self.scope["user"], AnonymousUser):
            return
        self.user = self.scope['user']

        self.chat_room = f'chat_room_{self.user.id}'
        
        await self.channel_layer.group_add(
            self.chat_room,
            self.channel_name
        )
        await self.accept()

    async def receive_json(self, content, **kwargs):
        message = content.get("message")
        thread_id = content.get("thread_id")
        thread = await self.get_thread(thread_id)
        other_user_chatroom = await self.get_other_user_chatroom(thread)

        response = await self.save_message(message,thread)

        await self.channel_layer.group_send(
            other_user_chatroom,
            {
                "type":"chat_message",
                "message":response,
            }
        )
        await self.channel_layer.group_send(
            self.chat_room,
            {
                "type":"chat_message",
                "message":response,
            }
        )

    async def disconnect(self, code):
        if hasattr(self, "chat_room"):
            await self.channel_layer.group_discard(
                self.chat_room,
                self.channel_name
            )
        return await super().disconnect(code)
    
    async def chat_message(self,event):
        message = event['message']
        await self.send_json(message)

    @database_sync_to_async
    def get_thread(self, thread_id):
        return MessageThread.objects.get(id = thread_id)
    
    @sync_to_async
    def get_other_user_chatroom(self, thread):
        if thread.first_user == self.user:
            return f'chat_room_{thread.second_user.id}'
        else:
            return f'chat_room_{thread.first_user.id}'
    
    @database_sync_to_async
    def save_message(self, message, thread):
        user = self.user
        msg_obj =  Message.objects.create(thread = thread, sent_by= user, message = message)
        return MessageSerializer(msg_obj).data

#?sourceId=src_AOFz4gOeuHY7zZesvDExh