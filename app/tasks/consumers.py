from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
from django.db import models
from tasks.models import Task


class TaskNotificationConsumer(JsonWebsocketConsumer):
    def connect(self):
        user = self.scope["user"]
        if not user.is_authenticated:
            self.disconnect()
        if not user.is_superuser:
            staff_or_normal_user_q = (
                models.Q(reporter=user) if user.is_staff else models.Q(assignee=user)
            )
            related_tasks_ids = (
                Task.objects.filter(
                    staff_or_normal_user_q | models.Q(watchers__id=user.id)
                )
                .distinct()
                .values_list("id", flat=True)
            )
        else:
            related_tasks_ids = Task.objects.values_list("id", flat=True)

        for task_id in related_tasks_ids:
            task_group_name = f"task_{task_id}"
            async_to_sync(self.channel_layer.group_add)(
                task_group_name, self.channel_name
            )

        self.accept()

    def task_notification(self, event_content):
        self.send_json(content=event_content)
