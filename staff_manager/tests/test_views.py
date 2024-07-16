from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import reverse

from content.models import ContentType, Task
from staff_manager.forms import PositionSearchForm, StaffSearchForm
from staff_manager.models import Position
from staff_manager.views import PositionListView, StaffListView

POSITION_URL = reverse("positions:position-list")
STAFF_URL = reverse("staff:staff-list")


class PublicPositionViewTest(TestCase):
    def test_login_required(self):
        response = self.client.get(POSITION_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivatePositionViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test1234"
        )
        self.client.force_login(self.user)
        self.test_name = "Actor"
        Position.objects.create(name=self.test_name)
        Position.objects.create(name="Director")

    def test_retrieve_positions(self):
        positions = Position.objects.all()
        response = self.client.get(POSITION_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["position_list"]),
            list(positions)
        )

    def test_position_search_form_is_present(self):
        search_form = PositionSearchForm()
        response = self.client.get(POSITION_URL)
        self.assertIsInstance(
            response.context["search_form"],
            type(search_form)
        )

    def test_position_get_queryset(self):
        request = RequestFactory().get(f"positions/?name={self.test_name}")
        view = PositionListView()
        view.request = request
        queryset = view.get_queryset()
        self.assertQuerysetEqual(
            queryset,
            Position.objects.filter(name=self.test_name)
        )


class PublicStaffViewTest(TestCase):
    def test_login_required(self):
        response = self.client.get(STAFF_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateStaffViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test1234"
        )
        self.client.force_login(self.user)
        self.test_username = "test_search_user"
        self.test_first_name = "John"
        self.test_last_name = "Doe"
        get_user_model().objects.create_user(
            username=self.test_username,
            password="test1234",
            first_name=self.test_first_name,
            last_name=self.test_last_name
        )

    def test_retrieve_staff(self):
        staff = get_user_model().objects.all()
        response = self.client.get(STAFF_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["staff_list"]),
            list(staff)
        )

    def test_staff_search_form_is_present(self):
        search_form = StaffSearchForm()
        response = self.client.get(STAFF_URL)
        self.assertIsInstance(
            response.context["search_form"],
            type(search_form)
        )

    def test_staff_get_queryset(self):
        view = StaffListView()
        request = RequestFactory().get(f"staff/?staff={self.test_username}")
        view.request = request
        queryset = view.get_queryset()
        self.assertQuerysetEqual(
            queryset,
            get_user_model().objects.filter(username=self.test_username)
        )

        request = RequestFactory().get(f"staff/?staff={self.test_first_name}")
        view.request = request
        queryset = view.get_queryset()
        self.assertQuerysetEqual(
            queryset,
            get_user_model().objects.filter(first_name=self.test_first_name)
        )

        request = RequestFactory().get(f"staff/?staff={self.test_last_name}")
        view.request = request
        queryset = view.get_queryset()
        self.assertQuerysetEqual(
            queryset,
            get_user_model().objects.filter(last_name=self.test_last_name)
        )

    def test_staff_has_unfinished_tasks_in_detail_view_context(self):
        ContentType.objects.create(name="presentation")
        task = Task.objects.create(
            name="Test task",
            deadline=date(2024, 7, 30),
            content_type_id=1
        )
        task.staff.add(self.user)
        user_tasks = Task.objects.filter(staff=self.user)

        response = self.client.get(reverse("staff:staff-detail", args=[1]))
        self.assertQuerysetEqual(
            response.context["unfinished_tasks"],
            user_tasks
        )
