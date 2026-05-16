from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN = "ADMIN"
    USER = "USER"

    ROLE_CHOICES = [
        (ADMIN, "Admin"),
        (USER, "User"),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=USER,
        db_index=True,
    )

    email = models.EmailField(unique=True)

    REQUIRED_FIELDS = ["email"]

    class Meta:
        indexes = [
            models.Index(fields=["role"]),
            models.Index(fields=["email"]),
        ]

    def __str__(self):
        return f"{self.username} - {self.role}"