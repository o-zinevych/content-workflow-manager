from django import template

register = template.Library()


@register.simple_tag
def form_check(request):
    return "create" in request.path or "update" in request.path
