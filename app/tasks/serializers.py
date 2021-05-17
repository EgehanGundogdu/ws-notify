from rest_framework import serializers
from tasks.models import Task


class TaskDetailSerializer(serializers.ModelSerializer):
    watchers = serializers.SlugRelatedField(
        slug_field="full_name", read_only=True, many=True
    )
    assignee = serializers.SlugRelatedField(read_only=True, slug_field="full_name")
    reporter = serializers.SlugRelatedField(read_only=True, slug_field="full_name")

    class Meta:
        model = Task
        fields = "__all__"