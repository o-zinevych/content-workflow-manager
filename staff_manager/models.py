from django.contrib.auth.models import AbstractUser
from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Staff(AbstractUser):
    position = models.ManyToManyField(Position, related_name="staff")

    class Meta:
        verbose_name_plural = "staff"

    def __str__(self):
        positions = ", ".join([pos.name for pos in self.position.all()])
        if self.first_name and self.last_name:
            return (f"{self.first_name} {self.last_name} "
                    f"({positions}, @{self.username})")
        return f"{self.username} ({positions})"
