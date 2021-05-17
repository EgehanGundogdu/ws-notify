from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from tasks.mixins import FormViewsButtonLabelContextMixin, StaffRequiredMixin
from tasks.models import Task
from rest_framework.generics import RetrieveAPIView

from tasks.serializers import TaskDetailSerializer


class TaskCreateView(
    LoginRequiredMixin,
    StaffRequiredMixin,
    FormViewsButtonLabelContextMixin,
    CreateView,
):
    button_label_text = "Create new task."
    model = Task
    fields = "__all__"


class TaskUpdateView(
    LoginRequiredMixin,
    StaffRequiredMixin,
    FormViewsButtonLabelContextMixin,
    UpdateView,
):
    button_label_text = "Update task."
    model = Task
    fields = "__all__"


class TaskDetailView(LoginRequiredMixin, RetrieveAPIView):
    model = Task
    serializer_class = TaskDetailSerializer
    queryset = Task.objects.all()

class TaskListView(LoginRequiredMixin, ListView):
    model = Task

    def get_queryset(self) -> models.QuerySet:
        user = self.request.user
        staff_or_normal_user_query = (
            models.Q(reporter=user) if user.is_staff else models.Q(assignee=user)
        )
        related_tasks = Task.objects.filter(
            staff_or_normal_user_query | models.Q(watchers=user)
        ).distinct()
        return related_tasks
