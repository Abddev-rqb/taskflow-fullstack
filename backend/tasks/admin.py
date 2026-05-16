from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "assigned_to",
        "created_by",
        "status",
        "priority",
        "due_date",
        "created_at",
    )
    list_filter = ("status", "priority", "due_date", "created_at")
    search_fields = ("title", "description", "assigned_to__username", "created_by__username")
    ordering = ("-created_at",)