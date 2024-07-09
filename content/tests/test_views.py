from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from content.models import ContentType, Task

INDEX_URL = reverse("content:index")
CONTENT_TYPE_URL = reverse("content:content-type-list")


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
