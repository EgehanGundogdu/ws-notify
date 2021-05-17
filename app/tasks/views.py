from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from tasks.mixins import FormViewsButtonLabelContextMixin, StaffRequiredMixin
from tasks.models import Task
from rest_framework.generics import RetrieveAPIView
from tasks.notifier import TaskNotifier

from tasks.serializers import TaskDetailSerializer
from django.urls import reverse_lazy


class TaskCreateView(
    LoginRequiredMixin,
    StaffRequiredMixin,
    FormViewsButtonLabelContextMixin,
    CreateView,
):
    button_label_text = "Create new task."
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("tasks:task-list")


class TaskUpdateView(
    LoginRequiredMixin,
    StaffRequiredMixin,
    FormViewsButtonLabelContextMixin,
    UpdateView,
):
    button_label_text = "Update task."
    model = Task
    fields = "__all__"
    notifier = TaskNotifier()
    success_url = reverse_lazy("tasks:task-list")

    def form_valid(self, form):
        response = super().form_valid(form)
        group_name = f"task_{form.instance.id}"
        notification_content = {
            "user": self.request.user.full_name,
            "message": f"{form.instance.title.title()} updated",
            "action_date": form.instance.modified_at.__str__(),
        }
        self.notifier.send_notification(
            group_name=group_name, type="task_notification", **notification_content
        )
        return response


class TaskDetailView(LoginRequiredMixin, RetrieveAPIView):
    model = Task
    serializer_class = TaskDetailSerializer
    queryset = Task.objects.all()


class TaskListView(LoginRequiredMixin, ListView):
    model = Task

    def get_queryset(self) -> models.QuerySet:
        user = self.request.user
        if user.is_superuser:
            return Task.objects.all()
        else:
            staff_or_normal_user_query = (
                models.Q(reporter=user) if user.is_staff else models.Q(assignee=user)
            )
            related_tasks = Task.objects.filter(
                staff_or_normal_user_query | models.Q(watchers=user)
            ).distinct()
            return related_tasks
