from django.urls import path
from channels.routing import URLRouter

from comments.routing import websocket_urlpatterns as comment_urls

websocket_urlpatterns = [
    path('ws/', URLRouter([
        *comment_urls,
        ])
    ),
]
