import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Notification

class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        if self.user.is_anonymous:
            self.close()
        else:
            self.group_name = f"notifications_{self.user.id}"
            async_to_sync(self.channel_layer.group_add)(
                self.group_name,
                self.channel_name
            )
            self.accept()

    def disconnect(self, close_code):
        if not self.user.is_anonymous:
            async_to_sync(self.channel_layer.group_discard)(
                self.group_name,
                self.channel_name
            )

    def receive(self, text_data):
        data = json.loads(text_data)
        # Mark notifications as read in the database
        if data.get('type') == 'mark_as_read':
            Notification.objects.filter(user=self.user, is_read=False).update(is_read=True)

    def send_notification(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'message': message
        }))


        