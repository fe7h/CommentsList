from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer


class CommentsConsumer(JsonWebsocketConsumer):
    tracked_branches = None

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
        print(self.tracked_branches, type(self.tracked_branches))

        # async_to_sync(self.channel_layer.group_send)(
        #     'connect',
        #     {
        #         'type': 'new_comment',
        #         'comment': comment,
        #     }
        # )

    def new_comment(self, event):
        comment = event['comment']

        self.send_json({
            "comment": comment
        })
