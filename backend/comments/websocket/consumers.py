from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

from comments.api.serializers import CommentPolymorphicSerializer


class CommentsConsumer(JsonWebsocketConsumer):
    tracked_branches = []

    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            'connect',
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            'connect',
            self.channel_name
        )

    def receive_json(self, content, **kwargs):
        self.tracked_branches = content.get('tracked_branches')

    def new_comment(self, event):
        comment = event['comment']
        response = {}

        if not hasattr(comment, 'parent_comment_id') or str(comment.parent_comment_id) in self.tracked_branches:
            response['comment'] = CommentPolymorphicSerializer(comment).data

            self.send_json({
                **response
            })
