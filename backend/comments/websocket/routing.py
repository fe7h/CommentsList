from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('connect/', consumers.CommentsConsumer.as_asgi()),
]
