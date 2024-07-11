from django.contrib.auth.models import AbstractUser
from django.db import models

from content_workflow_manager import settings


class ContentType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Task(models.Model):
    PRIORITIES = [
        ("0", "low"),
        ("1", "medium"),
        ("2", "high"),
        ("3", "urgent")
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    deadline = models.DateField()
    is_finished = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=1,
        choices=PRIORITIES,
        default="0"
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    staff = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="tasks"
    )

    class Meta:
        ordering = ["deadline", "priority"]

    def __str__(self):
        return f"{self.name} by {self.deadline}"
