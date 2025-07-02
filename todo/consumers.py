import json
from channels.generic.websocket import WebsocketConsumer

class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        print(f"WebSocket connected: {self.channel_name}") # Debug print
        self.channel_layer.group_add(
            "websocket_notifications",
            self.channel_name
        )

    def disconnect(self, close_code):
        self.channel_layer.group_discard(
            "websocket_notifications",
            self.channel_name
        )

    def receive(self, text_data):
        pass

    def send_notification(self, event):
        message = event['message']
        print(f"Sending notification: {message}") # Debug print
        self.send(text_data=json.dumps({
            'message': message
        }))
