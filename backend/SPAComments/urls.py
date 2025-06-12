from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from comments.api.urls import urlpatterns as comment_urls
from comments.urls import urlpatterns as csrf_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('', include(comment_urls)),
        path('', include(csrf_urls)),
        ])
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
