from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase

from content.models import ContentType, Position, Task


class TestContentTypeModel(TestCase):
    def test_content_type_str(self):
        content_type = ContentType.objects.create(name="Test Type")
        self.assertEqual(str(content_type), content_type.name)


class TestPositionModel(TestCase):
    def test_position_str(self):
        position = Position.objects.create(name="Trainee")
        self.assertEqual(str(position), position.name)


class TestStaffModel(TestCase):
    def setUp(self):
        self.position1 = Position.objects.create(name="First Position")
        self.position2 = Position.objects.create(name="Second Position")
        self.staff = get_user_model().objects.create_user(
            username="test_username",
            password="test1234",
        )
        self.staff.position.add(self.position1, self.position2)
        self.positions = ", ".join(
            [pos.name for pos in self.staff.position.all()]
        )

    def test_staff_with_no_names_str(self):
        self.assertEqual(
            str(self.staff),
            f"{self.staff.username} ({self.positions})"
        )

    def test_staff_with_names_str(self):
        self.staff.first_name = "Test"
        self.staff.last_name = "User"
        self.assertEqual(
            str(self.staff),
            f"{self.staff.first_name} {self.staff.last_name} "
            f"({self.positions}, @{self.staff.username})"
        )


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
