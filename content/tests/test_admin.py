from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from content.admin import StaffAdmin, TaskAdmin
from content.models import Position, Task, ContentType


class StaffAdminPanelTest(TestCase):
    def setUp(self):
        self.position1 = "Moderator"
        self.position2 = "Administrator"
        position1 = Position.objects.create(name=self.position1)
        position2 = Position.objects.create(name=self.position2)
        self.admin_user = get_user_model().objects.create_superuser(
            username="test_admin",
            password="test1234",
        )
        self.admin_user.position.add(position1, position2)
        self.client.force_login(self.admin_user)

    def test_staff_queryset(self):
        response = self.client.get(reverse("admin:content_staff_changelist"))
        queryset = response.context["cl"].queryset
        self.assertIn("position", queryset._prefetch_related_lookups)

    def test_staff_position_field(self):
        admin_instance = StaffAdmin(model=get_user_model(), admin_site=None)
        staff_position = admin_instance.staff_position(self.admin_user)
        self.assertEqual(staff_position, f"{self.position2}, {self.position1}")


class TaskAdminPanelTest(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="test_admin",
            password="test1234",
        )
        self.client.force_login(self.admin_user)
        self.content_type_name = "Test"
        content_type = ContentType.objects.create(name=self.content_type_name)
        self.staff = get_user_model().objects.create_user(
            username="test_staff",
            password="qwerty4321",
        )
        self.task = Task.objects.create(
            deadline=date(2024, 7, 20),
            content_type=content_type,
        )
        self.task.staff.add(self.admin_user, self.staff)

    def test_task_queryset(self):
        response = self.client.get(reverse("admin:content_task_changelist"))
        queryset = response.context["cl"].queryset
        self.assertIn("content_type", queryset.query.select_related)

    def test_staff_involved_field(self):
        admin_instance = TaskAdmin(model=Task, admin_site=None)
        staff_involved = admin_instance.staff_involved(self.task)
        self.assertEqual(
            staff_involved,
            f"{self.admin_user.username}, {self.staff.username}"
        )
