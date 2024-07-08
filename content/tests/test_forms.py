from django.test import TestCase

from content.forms import (
    ContentTypeForm,
)


class ContentTypeFormTest(TestCase):
    def test_content_type_form_is_valid(self):
        form_data = {"name": "article"}
        form = ContentTypeForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_name_must_be_lowercase(self):
        form_data = {"name": "Article"}
        form = ContentTypeForm(data=form_data)
        self.assertFalse(form.is_valid())
