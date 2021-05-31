from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/lab/(?P<article_id>\w+)/$', consumers.ChatConsumer.as_asgi()),
    path('ws/lab/tasks/', consumers.TasksConsumer.as_asgi()),
]
