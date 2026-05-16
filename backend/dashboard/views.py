from django.utils import timezone
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from tasks.models import Task


class IsAdminRole(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == User.ADMIN
        )


class AdminDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminRole]

    def get(self, request):
        total_users = User.objects.filter(role=User.USER).count()
        total_admins = User.objects.filter(role=User.ADMIN).count()

        total_tasks = Task.objects.count()
        pending_tasks = Task.objects.filter(status=Task.PENDING).count()
        in_progress_tasks = Task.objects.filter(status=Task.IN_PROGRESS).count()
        completed_tasks = Task.objects.filter(status=Task.COMPLETED).count()
        high_priority_tasks = Task.objects.filter(priority=Task.HIGH).count()
        overdue_tasks = Task.objects.filter(
            due_date__lt=timezone.localdate()
        ).exclude(status=Task.COMPLETED).count()

        return Response(
            {
                "total_users": total_users,
                "total_admins": total_admins,
                "total_tasks": total_tasks,
                "pending_tasks": pending_tasks,
                "in_progress_tasks": in_progress_tasks,
                "completed_tasks": completed_tasks,
                "high_priority_tasks": high_priority_tasks,
                "overdue_tasks": overdue_tasks,
            }
        )


class UserDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        user_tasks = Task.objects.filter(assigned_to=user)

        total_tasks = user_tasks.count()
        pending_tasks = user_tasks.filter(status=Task.PENDING).count()
        in_progress_tasks = user_tasks.filter(status=Task.IN_PROGRESS).count()
        completed_tasks = user_tasks.filter(status=Task.COMPLETED).count()
        high_priority_tasks = user_tasks.filter(priority=Task.HIGH).count()

        upcoming_due_tasks = user_tasks.filter(
            due_date__gte=timezone.localdate()
        ).exclude(status=Task.COMPLETED).order_by("due_date")[:5]

        upcoming_due_tasks_data = [
            {
                "id": task.id,
                "title": task.title,
                "status": task.status,
                "priority": task.priority,
                "due_date": task.due_date,
            }
            for task in upcoming_due_tasks
        ]

        return Response(
            {
                "total_tasks": total_tasks,
                "pending_tasks": pending_tasks,
                "in_progress_tasks": in_progress_tasks,
                "completed_tasks": completed_tasks,
                "high_priority_tasks": high_priority_tasks,
                "upcoming_due_tasks": upcoming_due_tasks_data,
            }
        )