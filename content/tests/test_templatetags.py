from django.template import Context, Template
from django.test import TestCase, RequestFactory


class FormCheckTagTest(TestCase):
    def setUp(self):
        self.template = Template(
            "{% load form_check %}"
            "{% form_check request as is_form %}"
            "{% if request.path == '/staff/' or is_form %}"
            "<nav id='navbar-main' aria-label='Primary navigation' "
            "class='navbar navbar-main navbar-expand-lg navbar-theme-primary "
            "headroom navbar-light navbar-theme-secondary'>"
            "{% else %}"
            "<nav id='navbar-main' aria-label='Primary navigation' "
            "class='navbar navbar-main navbar-expand-lg navbar-theme-primary "
            "headroom navbar-dark navbar-theme-secondary'>"
            "{% endif %}"
        )

    def test_light_navbar_rendered(self):
        request_light = RequestFactory().get("/positions/create/")
        context = Context({"request": request_light})
        rendered = self.template.render(context=context)
        self.assertIn("navbar-light", rendered)

    def test_dark_navbar_rendered(self):
        request_dark = RequestFactory().get("/positions/")
        context = Context({"request": request_dark})
        rendered = self.template.render(context=context)
        self.assertIn("navbar-dark", rendered)
