from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_task_assignment_email(task_id, task_title, assigned_to_email, assigned_to_username):
    subject = f"New Task Assigned: {task_title}"

    message = f"""
Hello {assigned_to_username},

A new task has been assigned to you.

Task ID: {task_id}
Task Title: {task_title}

Please login to TaskFlow and check your task dashboard.

Regards,
TaskFlow Team
"""

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[assigned_to_email],
        fail_silently=False,
    )

    return f"Task assignment email sent to {assigned_to_email}"