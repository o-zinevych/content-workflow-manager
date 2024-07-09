from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import reverse

from content.forms import PositionSearchForm, StaffSearchForm
from content.models import ContentType, Task, Position
from content.views import PositionListView, StaffListView

INDEX_URL = reverse("content:index")
CONTENT_TYPE_URL = reverse("content:content-type-list")
POSITION_URL = reverse("content:position-list")
STAFF_URL = reverse("content:staff-list")
TASK_URL = reverse("content:task-list")


class PublicIndexViewTest(TestCase):
    def test_login_required(self):
        response = self.client.get(INDEX_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateIndexViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test1234"
        )
        self.client.force_login(self.user)

    def test_retrieve_index_statistics(self):
        ContentType.objects.create(name="article")
        ContentType.objects.create(name="short-form video")
        get_user_model().objects.create_user(
            username="test_user2",
            password="test1234"
        )
        Task.objects.create(
                    name="Test task",
                    deadline=date(2024, 7, 25),
                    content_type_id=1
                )
        Task.objects.create(
                    name="Another test task",
                    deadline=date(2024, 7, 30),
                    content_type_id=2
                )
        response = self.client.get(INDEX_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "content/index.html")
        self.assertContains(response, ContentType.objects.count())
        self.assertContains(response, get_user_model().objects.count())
        self.assertContains(response, Task.objects.count())


class PublicContentTypeViewTest(TestCase):
    def test_login_required(self):
        response = self.client.get(CONTENT_TYPE_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateContentTypeViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test1234"
        )
        self.client.force_login(self.user)

    def test_retrieve_content_types(self):
        ContentType.objects.create(name="article")
        ContentType.objects.create(name="long-form video")
        content_types = ContentType.objects.all()

        response = self.client.get(CONTENT_TYPE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["content_type_list"]),
            list(content_types)
        )


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

        response = self.client.get(reverse("content:staff-detail", args=[1]))
        self.assertQuerysetEqual(
            response.context["unfinished_tasks"],
            user_tasks
        )


class PublicTaskViewTest(TestCase):
    def test_login_required(self):
        response = self.client.get(STAFF_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateTaskViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test1234"
        )
        self.client.force_login(self.user)

        ContentType.objects.create(name="article")
        self.test_name = "Test task"
        task = Task.objects.create(
            name=self.test_name,
            deadline=date(2024, 7, 29),
            content_type_id=1
        )
        task.staff.add(self.user)

    def test_retrieve_tasks(self):
        tasks = Task.objects.all()
        response = self.client.get(TASK_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["task_list"]),
            list(tasks)
        )
