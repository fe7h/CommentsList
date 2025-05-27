from django.contrib import admin
from django.urls import path, include

from comments.api.urls import urlpatterns as comment_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(comment_urls)),
]
