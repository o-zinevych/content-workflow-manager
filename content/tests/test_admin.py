from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from content.admin import TaskAdmin
from content.models import Task, ContentType


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
