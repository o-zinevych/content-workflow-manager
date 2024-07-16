from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import reverse

from content.forms import TaskSearchForm
from content.models import ContentType, Task
from content.views import TaskListView

INDEX_URL = reverse("content:index")
CONTENT_TYPE_URL = reverse("content:content-type-list")
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


class PublicTaskViewTest(TestCase):
    def test_login_required(self):
        response = self.client.get(TASK_URL)
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
        self.task = Task.objects.create(
            name=self.test_name,
            deadline=date(2024, 7, 29),
            content_type_id=1
        )
        self.task.staff.add(self.user)

    def test_retrieve_tasks(self):
        tasks = Task.objects.all()
        response = self.client.get(TASK_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["task_list"]),
            list(tasks)
        )

    def test_task_search_form_is_present(self):
        search_form = TaskSearchForm()
        response = self.client.get(TASK_URL)
        self.assertIsInstance(
            response.context["search_form"],
            type(search_form)
        )

    def test_task_get_queryset(self):
        view = TaskListView()
        request = RequestFactory().get(f"tasks/?name={self.test_name}")
        view.request = request
        queryset = view.get_queryset()
        self.assertQuerysetEqual(
            queryset,
            Task.objects.filter(name=self.test_name)
        )

        request = RequestFactory().get(f"tasks/?name={self.user.username}")
        view.request = request
        queryset = view.get_queryset()
        self.assertQuerysetEqual(
            queryset,
            Task.objects.filter(staff=self.user)
        )

    def test_task_staff_deletion_and_assignment_button(self):
        response = self.client.get(TASK_URL)
        self.assertIn(
            "/update-staff/",
            response.rendered_content
        )

        self.client.get(reverse("content:task-staff-update", args=[1]))
        self.assertNotIn(
            self.user,
            self.task.staff.all(),
            "User must be removed from the task staff list"
        )

        self.client.get(reverse("content:task-staff-update", args=[1]))
        self.assertIn(
            self.user,
            self.task.staff.all(),
            "User must be added to task staff list"
        )
