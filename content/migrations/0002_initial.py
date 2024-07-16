# Generated by Django 5.0.6 on 2024-07-11 16:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("content", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="staff",
            field=models.ManyToManyField(
                related_name="tasks", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
