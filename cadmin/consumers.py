
from channels.generic.websocket import AsyncJsonWebsocketConsumer

import asyncio

from .models import  Group, Chat
from client.models import TherapySessions

from client.models import User

from channels.db import database_sync_to_async


class MyAsyncJsonWebsocketConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        print("Websocket connected")
        print("Channel Layer... ", self.channel_layer)
        print("Channel Name... ", self.channel_name)

        self.group_name = self.scope['url_route']['kwargs']['group_name']

        # self.group_name = TherapySessions.objects.get()
        self.user_id = self.scope['url_route']['kwargs']['user_id']

        # print(self.user_id)
        # print(type(self.user_id))

        print("Group Name ; ", self.group_name)

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()


    async def receive_json(self, content, **kwargs):
        print("Message received from client...", content)

        group = await database_sync_to_async(Group.objects.get_or_create)(name=self.group_name)
        print("slgkjspogijs", group)
        group_id = group[0].id
        print(group_id)
        group = await database_sync_to_async(Group.objects.filter(id=group_id).first)()

        user = await database_sync_to_async(User.objects.get)(id=self.user_id)
       
        print(user)

        chat = Chat(
            content = content["msg"], 
            group = group,
            owner = user
        )

        await database_sync_to_async(chat.save)()
        print("The girl who fell in love... ", content['msg'])

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat.message',
                'message': content["msg"],
                'owner': user.id
            }
        )
    
    async def chat_message(self, event):
        print("Event...", event)

        await self.send_json({
            'message':event['message'], 
            'owner': event['owner']
        })

   


    async def disconnect(self, code):
        print("Websocket disconnected...", code)
        print("Channel Layer... ", self.channel_layer)
        print("Channel Name... ", self.channel_name)

        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
   