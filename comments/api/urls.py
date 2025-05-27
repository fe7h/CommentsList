from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r'test', views.CommentView, basename='test')

urlpatterns = [
    path('', include(router.urls))
]
