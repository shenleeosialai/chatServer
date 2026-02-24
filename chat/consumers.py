import json
from asgiref.sync import async_to_async
from django.utils import timezone
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):    
    def connect(self):
        self.user = self.scope['user']
        self.id = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = f'chat_{self.id}'
        # Join room group
        async_to_async(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
    
    def disconnect(self, close_code):
        # Leave room group
        async_to_async(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )    
    
    def receive(self , text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        now = timezone.now()
        async_to_async(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.user.username,
                'timestamp': now.isoformat(),
                
            }
        )
    
    # Receive message from room group
    def chat_message(self, event):
        # Send message to WebSocket
        self.send(text_data=json.dumps(event))