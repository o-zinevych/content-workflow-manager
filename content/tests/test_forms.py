from django.test import TestCase

from content.forms import (
    ContentTypeForm,
    PositionForm,
    PositionSearchForm,
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


class PositionFormsTest(TestCase):
    def test_position_form_is_valid(self):
        form_data = {"name": "Actor"}
        form = PositionForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_position_name_must_be_title_case(self):
        form_data = {"name": "actor"}
        form = PositionForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_position_search_form_is_valid(self):
        form_data = {"name": "act"}
        form = PositionSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
