from django.contrib.auth.models import AbstractUser
from django.db import models


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
