import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Messages, MessageInstances, Users, Groups, GroupMessage
from django.utils import timezone


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

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

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type', 'text_message')

        if message_type == 'text_message':
            await self.handle_text_message(data)
        elif message_type == 'delete_message':
            await self.handle_delete_message(data)

    async def handle_text_message(self, data):
        message = data['message']
        incoming = data['incoming']
        outgoing = data['outgoing']
        date = data.get('date')
        time = data.get('time')

        # Save message to database
        message_data = await self.save_message(message, incoming, outgoing, date, time)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'incoming': incoming,
                'outgoing': outgoing,
                'message_id': message_data['message_id'],
                'date': date,
                'time': time,
                'message_type': 'text'
            }
        )

    async def handle_delete_message(self, data):
        message_id = data['message_id']
        
        # Delete message from database
        await self.delete_message(message_id)

        # Notify room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'message_deleted',
                'message_id': message_id
            }
        )

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message'],
            'incoming': event['incoming'],
            'outgoing': event['outgoing'],
            'message_id': event['message_id'],
            'date': event['date'],
            'time': event['time'],
            'message_type': event['message_type']
        }))

    async def message_deleted(self, event):
        # Send delete notification to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'delete',
            'message_id': event['message_id']
        }))

    @database_sync_to_async
    def save_message(self, message, incoming, outgoing, date, time):
        incoming_user = Users.objects.get(username=incoming)
        outgoing_user = Users.objects.get(username=outgoing)
        
        try:
            last_id = MessageInstances.objects.last().id + 1
        except:
            last_id = 1

        message_instance = MessageInstances.objects.create(
            id=last_id,
            type='text',
            message=message,
            date=date,
            time=time
        )

        Messages.objects.create(
            incoming=incoming_user,
            outgoing=outgoing_user,
            message=message_instance
        )

        return {'message_id': message_instance.id}

    @database_sync_to_async
    def delete_message(self, message_id):
        try:
            MessageInstances.objects.get(id=message_id).delete()
        except:
            pass


class GroupChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'group_{self.room_name}'

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

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type', 'text_message')

        if message_type == 'text_message':
            await self.handle_text_message(data)
        elif message_type == 'delete_message':
            await self.handle_delete_message(data)

    async def handle_text_message(self, data):
        message = data['message']
        incoming = data['incoming']  # group name
        outgoing = data['outgoing']  # username
        date = data.get('date')
        time = data.get('time')

        # Save message to database
        message_data = await self.save_group_message(message, incoming, outgoing, date, time)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'group_message',
                'message': message,
                'incoming': incoming,
                'outgoing': outgoing,
                'message_id': message_data['message_id'],
                'date': date,
                'time': time,
                'message_type': 'text',
                'photo_url': message_data['photo_url']
            }
        )

    async def handle_delete_message(self, data):
        message_id = data['message_id']
        
        # Delete message from database
        await self.delete_message(message_id)

        # Notify room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'message_deleted',
                'message_id': message_id
            }
        )

    async def group_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message'],
            'incoming': event['incoming'],
            'outgoing': event['outgoing'],
            'message_id': event['message_id'],
            'date': event['date'],
            'time': event['time'],
            'message_type': event['message_type'],
            'photo_url': event['photo_url']
        }))

    async def message_deleted(self, event):
        # Send delete notification to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'delete',
            'message_id': event['message_id']
        }))

    @database_sync_to_async
    def save_group_message(self, message, incoming, outgoing, date, time):
        group = Groups.objects.get(name=incoming)
        user = Users.objects.get(username=outgoing)
        
        try:
            last_id = MessageInstances.objects.last().id + 1
        except:
            last_id = 1

        message_instance = MessageInstances.objects.create(
            id=last_id,
            type='text',
            message=message,
            date=date,
            time=time
        )

        GroupMessage.objects.create(
            incoming=group,
            outgoing=user,
            message=message_instance
        )

        return {
            'message_id': message_instance.id,
            'photo_url': user.photo.url if user.photo else ''
        }

    @database_sync_to_async
    def delete_message(self, message_id):
        try:
            MessageInstances.objects.get(id=message_id).delete()
        except:
            pass
