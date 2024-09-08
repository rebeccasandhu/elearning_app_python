import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import logging

logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.course_id = self.scope['url_route']['kwargs']['course_id']
        self.room_group_name = f'chat_{self.course_id}'

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
        text_data_json = json.loads(text_data)
        print(text_data_json)
        message = text_data_json.get('message')
        user_id = text_data_json.get('user_id')

        # Delayed import
        from .models import Comment, Course
        # Save the comment to the database
        if message and self.course_id and user_id:
            course = await self.get_course(self.course_id)
            user = await self.get_user(user_id)
            if course and user:
                comment = await self.create_comment(course, user, message)
                # Send comment to room group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': comment.content,
                        'first_name': comment.user.first_name,
                        'last_name': comment.user.last_name,
                        'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
                    }
                )

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'first_name': event['first_name'],
            'last_name': event['last_name'],
            'created_at': event['created_at'],
        }))

    @database_sync_to_async
    def get_course(self, course_id):
        from .models import Course  # Delayed import
        try:
            return Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return None

    @database_sync_to_async
    def get_user(self, user_id):
        from .models import User  # Delayed import
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    @database_sync_to_async
    def create_comment(self, course, user, content):
        from .models import Comment  # Delayed import
        return Comment.objects.create(course=course, user=user, content=content)