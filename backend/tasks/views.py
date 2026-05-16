from rest_framework import generics, permissions, status
from rest_framework.response import Response

from accounts.models import User
from .models import Task
from .serializers import TaskSerializer, TaskStatusUpdateSerializer
from .permissions import IsAdminRole, IsAdminOrAssignedUser
from .tasks import send_task_assignment_email


class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        queryset = Task.objects.select_related("assigned_to", "created_by").all()

        if user.role == User.USER:
            queryset = queryset.filter(assigned_to=user)

        status_filter = self.request.query_params.get("status")
        priority_filter = self.request.query_params.get("priority")
        assigned_to_filter = self.request.query_params.get("assigned_to")

        if status_filter:
            queryset = queryset.filter(status=status_filter)

        if priority_filter:
            queryset = queryset.filter(priority=priority_filter)

        if assigned_to_filter and user.role == User.ADMIN:
            queryset = queryset.filter(assigned_to_id=assigned_to_filter)

        return queryset

    def create(self, request, *args, **kwargs):
        if request.user.role != User.ADMIN:
            return Response(
                {"detail": "Only admin users can create tasks."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save(created_by=request.user)

        send_task_assignment_email.delay(
            task.id,
            task.title,
            task.assigned_to.email,
            task.assigned_to.username,
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrAssignedUser]

    def get_queryset(self):
        user = self.request.user

        queryset = Task.objects.select_related("assigned_to", "created_by").all()

        if user.role == User.USER:
            queryset = queryset.filter(assigned_to=user)

        return queryset

    def update(self, request, *args, **kwargs):
        if request.user.role != User.ADMIN:
            return Response(
                {"detail": "Only admin users can update full task details. Users can update status only."},
                status=status.HTTP_403_FORBIDDEN,
            )

        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if request.user.role != User.ADMIN:
            return Response(
                {"detail": "Only admin users can update full task details. Users can update status only."},
                status=status.HTTP_403_FORBIDDEN,
            )

        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if request.user.role != User.ADMIN:
            return Response(
                {"detail": "Only admin users can delete tasks."},
                status=status.HTTP_403_FORBIDDEN,
            )

        return super().destroy(request, *args, **kwargs)


class TaskStatusUpdateView(generics.UpdateAPIView):
    serializer_class = TaskStatusUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrAssignedUser]
    http_method_names = ["patch"]

    def get_queryset(self):
        user = self.request.user

        queryset = Task.objects.select_related("assigned_to", "created_by").all()

        if user.role == User.USER:
            queryset = queryset.filter(assigned_to=user)

        return queryset

    def patch(self, request, *args, **kwargs):
        task = self.get_object()

        serializer = self.get_serializer(task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": "Task status updated successfully",
                "task": TaskSerializer(task).data,
            },
            status=status.HTTP_200_OK,
        )