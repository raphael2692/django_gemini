from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Todo, Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

@receiver(post_save, sender=Todo)
def todo_saved(sender, instance, created, **kwargs):
    if created:
        message = f"New Todo created: {instance.title}"
    else:
        message = f"Todo updated: {instance.title}"

    Notification.objects.create(user=instance.user, message=message)

    channel_layer = get_channel_layer()
    group_name = f"notifications_{instance.user.id}"

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "send_notification",
            "message": message,
        }
    )