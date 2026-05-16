from rest_framework import serializers
from accounts.models import User
from accounts.serializers import UserSerializer
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    assigned_to_details = UserSerializer(source="assigned_to", read_only=True)
    created_by_details = UserSerializer(source="created_by", read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "assigned_to",
            "assigned_to_details",
            "created_by",
            "created_by_details",
            "status",
            "priority",
            "due_date",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_by", "created_at", "updated_at"]

    def validate_assigned_to(self, value):
        if value.role != User.USER:
            raise serializers.ValidationError("Tasks can only be assigned to users with USER role.")
        return value


class TaskStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["status"]

    def validate_status(self, value):
        allowed_statuses = [Task.PENDING, Task.IN_PROGRESS, Task.COMPLETED]

        if value not in allowed_statuses:
            raise serializers.ValidationError("Invalid task status.")

        return value