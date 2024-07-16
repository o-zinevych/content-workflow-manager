from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase

from content.models import ContentType, Task


class TestContentTypeModel(TestCase):
    def test_content_type_str(self):
        content_type = ContentType.objects.create(name="Test Type")
        self.assertEqual(str(content_type), content_type.name)


class TestTaskModel(TestCase):
    def test_task_str(self):
        content_type = ContentType.objects.create(name="Test Type")
        staff = get_user_model().objects.create_user(
            username="test_user",
            password="test1234"
        )
        task = Task.objects.create(
            name="Carry out some task",
            deadline=date(2024, 7, 20),
            content_type=content_type
        )
        task.staff.add(staff)
        self.assertEqual(str(task), f"{task.name} by {task.deadline}")
