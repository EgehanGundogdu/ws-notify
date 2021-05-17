from django.urls import path

from tasks.views import TaskCreateView, TaskDetailView, TaskListView, TaskUpdateView

app_name = "tasks"

urlpatterns = [
    path("", TaskListView.as_view(), name="task-list"),
    path("create/", TaskCreateView.as_view(), name="task-create"),
    path("update/<int:pk>/", TaskUpdateView.as_view(), name="task-update"),
    path("detail/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
]
