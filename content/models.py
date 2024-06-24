from django.contrib.auth.models import AbstractUser
from django.db import models

from content_workflow_manager import settings


class ContentType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]


class Position(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]


class Staff(AbstractUser):
    position = models.ManyToManyField(Position, related_name="staff")

    class Meta:
        verbose_name_plural = "staff"


class Task(models.Model):
    PRIORITIES = [
        ("0", "low"),
        ("1", "medium"),
        ("2", "high"),
        ("3", "urgent")
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
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
