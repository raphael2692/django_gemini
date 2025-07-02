from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Todo
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

@receiver(post_save, sender=Todo)
def todo_saved(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    if created:
        message = f"New Todo created: {instance.title}"
    else:
        message = f"Todo updated: {instance.title}"

    print(f"Signal triggered: {message}") # Debug print
    print(f"Channel layer type: {type(channel_layer)}") # New debug print

    async_to_sync(channel_layer.group_send)(
        "websocket_notifications",
        {
            "type": "send_notification",
            "message": message,
        }
    )
