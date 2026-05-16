import pytest
from rest_framework.test import APIClient

from accounts.models import User
from tasks.models import Task


@pytest.mark.django_db
class TestDashboardAPIs:
    def setup_method(self):
        self.client = APIClient()

        self.admin_user = User.objects.create_user(
            username="admin_dashboard_test",
            email="admin_dashboard_test@example.com",
            password="Admin@12345",
            role=User.ADMIN,
        )

        self.normal_user = User.objects.create_user(
            username="user_dashboard_test",
            email="user_dashboard_test@example.com",
            password="User@12345",
            role=User.USER,
        )

        Task.objects.create(
            title="Dashboard Task",
            description="Dashboard task description",
            assigned_to=self.normal_user,
            created_by=self.admin_user,
            status=Task.PENDING,
            priority=Task.HIGH,
            due_date="2026-05-25",
        )

    def test_admin_dashboard_accessible_by_admin(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.get("/api/dashboard/admin/")

        assert response.status_code == 200
        assert "total_users" in response.data
        assert "total_tasks" in response.data
        assert "overdue_tasks" in response.data

    def test_admin_dashboard_blocked_for_user(self):
        self.client.force_authenticate(user=self.normal_user)

        response = self.client.get("/api/dashboard/admin/")

        assert response.status_code == 403

    def test_user_dashboard_accessible_by_user(self):
        self.client.force_authenticate(user=self.normal_user)

        response = self.client.get("/api/dashboard/user/")

        assert response.status_code == 200
        assert response.data["total_tasks"] == 1
        assert response.data["pending_tasks"] == 1
        assert "upcoming_due_tasks" in response.data