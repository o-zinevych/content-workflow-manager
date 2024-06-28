from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from content.forms import PositionForm, StaffCreationForm
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


class ContentTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = ContentType
    fields = "__all__"
    template_name = "content/content_type_form.html"
    success_url = reverse_lazy("content:content-type-list")


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    paginate_by = 5


class PositionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Position
    queryset = Position.objects.prefetch_related("staff")


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = PositionForm
    template_name = "content/position_form.html"
    success_url = reverse_lazy("content:position-list")


class StaffListView(LoginRequiredMixin, generic.ListView):
    model = Staff
    queryset = get_user_model().objects.prefetch_related("position")
    paginate_by = 7


class StaffDetailView(LoginRequiredMixin, generic.DetailView):
    model = Staff
    queryset = get_user_model().objects.prefetch_related(
        "position",
        Prefetch("tasks", queryset=Task.objects.filter(is_finished=False))
    )

    def get_context_data(self, **kwargs):
        context = super(StaffDetailView, self).get_context_data(**kwargs)
        staff = self.get_object()
        unfinished_tasks = staff.tasks.filter(is_finished=False)
        context["unfinished_tasks"] = unfinished_tasks
        return context


class StaffCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = StaffCreationForm
    template_name = "content/staff_form.html"
    success_url = reverse_lazy("content:staff-list")


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    queryset = (Task.objects.select_related("content_type")
                .prefetch_related("staff"))


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    queryset = (Task.objects.select_related("content_type")
                .prefetch_related("staff"))
