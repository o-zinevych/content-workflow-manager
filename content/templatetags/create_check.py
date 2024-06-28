from django import template

register = template.Library()


@register.simple_tag
def create_check(request):
    return "create" in request.path
