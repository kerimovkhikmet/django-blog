import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.forms.models import model_to_dict
import datetime
from web_app.models import ConnectedUsers, Article, Commentary


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.article_id = self.scope['url_route']['kwargs']['article_id']
        self.article_group_name = 'chat_%s' % self.article_id

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.article_group_name,
            self.channel_name
        )
        username = f"Anonymous - {self.scope['client'][1]}" \
            if self.scope['user'].username == "" else self.scope['user'].username
        ConnectedUsers.objects.create(first_name=username)
        self.username = username
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.article_group_name,
            self.channel_name
        )
        ConnectedUsers.objects.filter(first_name=self.username).delete()

    # # Receive message from WebSocket
    def receive(self, text_data):
        data_json = json.loads(text_data)

        article = Article.objects.get(id=int(data_json['article_id']))
        username = f"Anonymous - {self.scope['client'][1]}" \
            if self.scope['user'].username == "" else self.scope['user'].username
        c = Commentary(article=article, text=data_json['commentText'], author=username)
        c.save()
        data_json = json.loads(json.dumps(model_to_dict(c)))
        data_json['date'] = c.date.strftime("%d.%m.%Y %H:%M")

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.article_group_name,
            {
                'type': 'chat_message',
                'entity_data': data_json
            }
        )
        
    # Receive message from room group
    def chat_message(self, event):
        entity_data = event['entity_data']
        print(entity_data)
        # Send message to WebSocket
        self.send(text_data=json.dumps(entity_data))


class TasksConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = "finished_tasks"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(text_data_json)
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'task_message',
                'message': message
            }
        )

    def task_message(self, event):
        message = event['message']
        print(message)

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
