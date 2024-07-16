from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from staff_manager.admin import StaffAdmin
from staff_manager.models import Position


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
        response = self.client.get(
            reverse("admin:staff_manager_staff_changelist")
        )
        queryset = response.context["cl"].queryset
        self.assertIn("position", queryset._prefetch_related_lookups)

    def test_staff_position_field(self):
        admin_instance = StaffAdmin(model=get_user_model(), admin_site=None)
        staff_position = admin_instance.staff_position(self.admin_user)
        self.assertEqual(staff_position, f"{self.position2}, {self.position1}")
