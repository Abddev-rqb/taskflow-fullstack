from unittest.mock import patch

import pytest
from rest_framework.test import APIClient

from accounts.models import User
from tasks.models import Task


@pytest.mark.django_db
class TestTaskAPIs:
    def setup_method(self):
        self.client = APIClient()

        self.admin_user = User.objects.create_user(
            username="admin_task_test",
            email="admin_task_test@example.com",
            password="Admin@12345",
            role=User.ADMIN,
        )

        self.normal_user = User.objects.create_user(
            username="user_task_test",
            email="user_task_test@example.com",
            password="User@12345",
            role=User.USER,
        )

        self.other_user = User.objects.create_user(
            username="other_user_test",
            email="other_user_test@example.com",
            password="User@12345",
            role=User.USER,
        )

        self.task = Task.objects.create(
            title="Existing Task",
            description="Existing task description",
            assigned_to=self.normal_user,
            created_by=self.admin_user,
            status=Task.PENDING,
            priority=Task.HIGH,
            due_date="2026-05-25",
        )

    @patch("tasks.views.send_task_assignment_email.delay")
    def test_admin_can_create_task(self, mock_delay):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.post(
            "/api/tasks/",
            {
                "title": "New Task",
                "description": "New task description",
                "assigned_to": self.normal_user.id,
                "status": Task.PENDING,
                "priority": Task.MEDIUM,
                "due_date": "2026-05-26",
            },
            format="json",
        )

        assert response.status_code == 201
        assert response.data["title"] == "New Task"
        assert response.data["assigned_to"] == self.normal_user.id
        mock_delay.assert_called_once()

    def test_user_cannot_create_task(self):
        self.client.force_authenticate(user=self.normal_user)

        response = self.client.post(
            "/api/tasks/",
            {
                "title": "Unauthorized Task",
                "description": "Should not be created",
                "assigned_to": self.normal_user.id,
                "status": Task.PENDING,
                "priority": Task.LOW,
                "due_date": "2026-05-26",
            },
            format="json",
        )

        assert response.status_code == 403

    def test_admin_can_view_all_tasks(self):
        Task.objects.create(
            title="Other User Task",
            description="Task assigned to other user",
            assigned_to=self.other_user,
            created_by=self.admin_user,
            status=Task.PENDING,
            priority=Task.LOW,
            due_date="2026-05-27",
        )

        self.client.force_authenticate(user=self.admin_user)

        response = self.client.get("/api/tasks/")

        assert response.status_code == 200
        assert len(response.data) == 2

    def test_user_can_view_only_assigned_tasks(self):
        Task.objects.create(
            title="Other User Task",
            description="Task assigned to other user",
            assigned_to=self.other_user,
            created_by=self.admin_user,
            status=Task.PENDING,
            priority=Task.LOW,
            due_date="2026-05-27",
        )

        self.client.force_authenticate(user=self.normal_user)

        response = self.client.get("/api/tasks/")

        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["assigned_to"] == self.normal_user.id

    def test_user_can_update_assigned_task_status(self):
        self.client.force_authenticate(user=self.normal_user)

        response = self.client.patch(
            f"/api/tasks/{self.task.id}/status/",
            {"status": Task.IN_PROGRESS},
            format="json",
        )

        assert response.status_code == 200
        assert response.data["task"]["status"] == Task.IN_PROGRESS

    def test_user_cannot_update_unassigned_task_status(self):
        other_task = Task.objects.create(
            title="Unassigned Task",
            description="Not assigned to normal user",
            assigned_to=self.other_user,
            created_by=self.admin_user,
            status=Task.PENDING,
            priority=Task.MEDIUM,
            due_date="2026-05-28",
        )

        self.client.force_authenticate(user=self.normal_user)

        response = self.client.patch(
            f"/api/tasks/{other_task.id}/status/",
            {"status": Task.IN_PROGRESS},
            format="json",
        )

        assert response.status_code == 404

    def test_user_cannot_delete_task(self):
        self.client.force_authenticate(user=self.normal_user)

        response = self.client.delete(f"/api/tasks/{self.task.id}/")

        assert response.status_code == 403

    def test_admin_can_delete_task(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.delete(f"/api/tasks/{self.task.id}/")

        assert response.status_code == 204