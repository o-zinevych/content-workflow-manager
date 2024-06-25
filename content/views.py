from django.shortcuts import render

from content.models import ContentType, Staff, Task


def index(request):
    """View function for the home page."""
    content_types_num = ContentType.objects.count()
    staff_num = Staff.objects.count()
    tasks_num = Task.objects.count()
    context = {
        "content_types_num": content_types_num,
        "staff_num": staff_num,
        "tasks_num": tasks_num,
    }
    return render(request, "content/index.html", context=context)
