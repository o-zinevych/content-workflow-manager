from django.db import models


class ContentType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]


class Position(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]
