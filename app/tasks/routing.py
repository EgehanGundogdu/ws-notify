from django.urls import path
from tasks.consumers import TaskNotificationConsumer


websocket_url_patterns = [
    path(
        "ws/tasks/",
        TaskNotificationConsumer.as_asgi(),
    )
]