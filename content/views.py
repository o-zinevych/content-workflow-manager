from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

from content.models import ContentType, Staff, Task, Position


@login_required
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


class ContentTypeListView(LoginRequiredMixin, generic.ListView):
    model = ContentType
    template_name = "content/content_type_list.html"
    context_object_name = "content_type_list"
    paginate_by = 5


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    paginate_by = 5


class StaffListView(LoginRequiredMixin, generic.ListView):
    model = Staff
    queryset = get_user_model().objects.prefetch_related("position")
    paginate_by = 7
