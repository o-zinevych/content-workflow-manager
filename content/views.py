from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from content.forms import (
    ContentTypeForm,
    PositionForm,
    PositionSearchForm,
    StaffChangeForm,
    StaffCreationForm,
    StaffSearchForm,
    TaskForm,
    TaskSearchForm,
)
from content.models import ContentType, Staff, Task, Position


@login_required
def index(request: HttpRequest) -> HttpResponse:
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


@login_required
def update_task_staff(request: HttpRequest, pk: int) -> HttpResponse:
    task = Task.objects.prefetch_related("staff").get(id=pk)
    if request.user in task.staff.all():
        task.staff.remove(request.user)
    else:
        task.staff.add(request.user)

    return redirect(reverse("content:task-list"), pk)


class ContentTypeListView(LoginRequiredMixin, generic.ListView):
    model = ContentType
    template_name = "content/content_type_list.html"
    context_object_name = "content_type_list"
    paginate_by = 5


class ContentTypeCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = ContentTypeForm
    template_name = "content/content_type_form.html"
    success_url = reverse_lazy("content:content-type-list")


class ContentTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = ContentType
    form_class = ContentTypeForm
    template_name = "content/content_type_form.html"
    success_url = reverse_lazy("content:content-type-list")


class ContentTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = ContentType
    template_name = "content/content_type_confirm_delete.html"
    success_url = reverse_lazy("content:content-type-list")


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PositionListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = PositionSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = Position.objects.all()
        name = self.request.GET.get("name")
        if name:
            name = name.title()
            return queryset.filter(name=name)
        return queryset


class PositionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Position
    queryset = Position.objects.prefetch_related("staff")


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = PositionForm
    template_name = "content/position_form.html"
    success_url = reverse_lazy("content:position-list")


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    form_class = PositionForm
    template_name = "content/position_form.html"
    success_url = reverse_lazy("content:position-list")


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("content:position-list")


class StaffListView(LoginRequiredMixin, generic.ListView):
    model = Staff
    paginate_by = 7

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(StaffListView, self).get_context_data(**kwargs)
        staff = self.request.GET.get("staff", "")
        context["search_form"] = StaffSearchForm(initial={"staff": staff})
        return context

    def get_queryset(self):
        queryset = get_user_model().objects.prefetch_related("position")
        staff = self.request.GET.get("staff")
        if staff:
            return queryset.filter(
                Q(username=staff) | Q(first_name=staff) | Q(last_name=staff)
            )
        return queryset


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


class StaffUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Staff
    form_class = StaffChangeForm
    template_name = "content/staff_form.html"
    success_url = reverse_lazy("content:staff-list")


class StaffDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Staff
    success_url = reverse_lazy("content:staff-list")


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = (Task.objects.select_related("content_type")
                    .prefetch_related("staff"))
        name = self.request.GET.get("name")
        if name:
            return queryset.filter(
                Q(name__icontains=name) | Q(staff__username__icontains=name)
            )
        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    queryset = (Task.objects.select_related("content_type")
                .prefetch_related("staff"))


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = TaskForm
    template_name = "content/task_form.html"
    success_url = reverse_lazy("content:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "content/task_form.html"
    success_url = reverse_lazy("content:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("content:task-list")
