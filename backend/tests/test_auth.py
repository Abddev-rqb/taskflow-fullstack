import pytest
from rest_framework.test import APIClient

from accounts.models import User


@pytest.mark.django_db
class TestAuthentication:
    def setup_method(self):
        self.client = APIClient()

        self.admin_user = User.objects.create_user(
            username="admin_test",
            email="admin_test@example.com",
            password="Admin@12345",
            role=User.ADMIN,
        )

        self.normal_user = User.objects.create_user(
            username="user_test",
            email="user_test@example.com",
            password="User@12345",
            role=User.USER,
        )

    def test_admin_login_returns_tokens(self):
        response = self.client.post(
            "/api/auth/login/",
            {
                "username": "admin_test",
                "password": "Admin@12345",
            },
            format="json",
        )

        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data
        assert response.data["user"]["role"] == User.ADMIN

    def test_user_login_returns_tokens(self):
        response = self.client.post(
            "/api/auth/login/",
            {
                "username": "user_test",
                "password": "User@12345",
            },
            format="json",
        )

        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data
        assert response.data["user"]["role"] == User.USER

    def test_profile_requires_authentication(self):
        response = self.client.get("/api/auth/profile/")

        assert response.status_code == 401

    def test_authenticated_user_can_view_profile(self):
        self.client.force_authenticate(user=self.normal_user)

        response = self.client.get("/api/auth/profile/")

        assert response.status_code == 200
        assert response.data["username"] == "user_test"
        assert response.data["role"] == User.USER

    def test_admin_can_view_users(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.get("/api/auth/users/")

        assert response.status_code == 200
        assert len(response.data) == 2

    def test_user_cannot_view_users(self):
        self.client.force_authenticate(user=self.normal_user)

        response = self.client.get("/api/auth/users/")

        assert response.status_code == 403