from django.db.models.signals import post_save

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import TopComment, NestedComment


def comment_saved(sender, instance, created, **kwargs):
    if created:
        async_to_sync(get_channel_layer().group_send)(
            'connect',
            {
                'type': 'new_comment',
                'comment': instance,
            }
        )


models_list = [TopComment, NestedComment]
for model in models_list:
    post_save.connect(comment_saved, sender=model)
