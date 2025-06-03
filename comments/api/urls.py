from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r'comments/top', views.TopCommentView, basename='top')
router.register(r'comments', views.CommentView, basename='comments')

urlpatterns = [
    path('', include(router.urls))
]
