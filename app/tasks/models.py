from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Create your models here.


class TaskStatuses(models.TextChoices):
    TODO = "todo", _("Todo")
    IN_PROGRESS = "in_progress", _("In Progress")
    DONE = "done", _("Done")


class Task(models.Model):
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tasks",
    )
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reported_tasks",
        limit_choices_to={"is_staff": True, "is_active": True},
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    watchers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, choices=TaskStatuses.choices, default=TaskStatuses.TODO
    )
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.title}"
